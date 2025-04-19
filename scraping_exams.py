import requests
import os
from bs4 import BeautifulSoup
from scraping_configs import user_agent

def get_plan_no(year, semester):
    print(f"Fetching plan number for year {year} semester {semester}...")
    session = requests.Session()

    # Step 1: Select General Access
    print("Accessing the General Access page...")
    url_step1 = "https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.MainSubmit"
    data_step1 = {
        "p_opt": "1",
        "p_type": "UE",
        "bOption": "Next"
    }
    header_step1 = {
        'User-Agent': user_agent,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = session.post(url_step1, data=data_step1 , headers=header_step1)
    response.raise_for_status()
    print("Inside General Access page\n")

    # Step 2: Extract plan number from radio button corresponding to target year/semester
    print("Extracting plan number...")
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup.prettify())
    radio_buttons  = soup.find_all("input", {"type": "radio", "name": "p_plan_no"})
    plan_options = []
    for radio in radio_buttons:
        value = radio['value']
        label = radio.next_sibling.strip() if radio.next_sibling else ''
        plan_options.append((value, label))

    print(f"Found {len(plan_options)} plan options:")
    for plan_no, label in plan_options:
        print(f"Plan No: {plan_no} - Label: {label}")

    target_label = f"AY{year}-{str(year+1)[-2:]} SEM {semester}".upper()
    for plan_no, label in plan_options:
        if label.upper() == target_label:
            print(f"Found matching plan_no: {plan_no} for {target_label}\n")
            return plan_no

    raise Exception(f"Could not find matching plan_no for {target_label}")


def fetch_exam_data(plan_no, year, semester, save_path="data/exams.html"):
    # Create the payload (equivalent to $request array)
    payload = {
        "p_exam_dt": "",
        "p_start_time": "",
        "p_dept": "",
        "p_subj": "",
        "p_venue": "",
        "p_plan_no": plan_no,
        "p_exam_yr": year,
        "p_semester": semester,
        "p_type": "UE",
        "academic_session": f"Semester {semester} Academic Year {str(year)}-{str(year + 1)}",
        "bOption": "Next"
    }

    # Make the HTTP request
    url = "https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.get_detail"
    response = requests.post(url, data=payload)

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Save the response HTML
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Saved to {save_path}")
    return response.text
year = 2024
semester = 2
plan_no = get_plan_no(year, semester)
print(f"Plan No for year {year} sem {semester}: {plan_no}")
fetch_exam_data(plan_no, year, semester)