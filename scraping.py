import requests, os
from scraping_configs import user_agent
from scraping_configs import user_agent, MODS_KEY, get_latest_semester, progress_semester

url = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"

def fetch_data(academic_year="2025", semester="1", save_folder="raw", file_name="mods.html"):
    values = {
            'r_search_type': 'F',
            'boption': 'Search',
            'acadsem': f"{academic_year};{semester}",
            'r_subj_code': '',
            'staff_access': 'false',
        }
    headers = {
        'User-Agent': user_agent,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    print("Fetching data")
    response = requests.post(url, data=values, headers=headers)
    print("Response code:", response.status_code)

    if response.status_code != 200:
        print("Failed to fetch data")
        return None
    if response.text.find("Class schedule is not available") != -1:
        print("No new data available")
        return None
    
    print("Data fetched successfully\n")
    
    # Save html file
    dir = os.path.join(save_folder, f"{academic_year}_{semester}")
    if save_folder != "":
        os.makedirs(dir, exist_ok=True)
    save_path = os.path.join(dir, file_name)
    with open(save_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"Saved to {save_path}")
    return response.text

if __name__ == "__main__":
    latest_sem = get_latest_semester(MODS_KEY)
    next_sem = latest_sem.next()
    print(f"Trying to fetch mods data for {next_sem}...")
    mod_data_html = fetch_data(next_sem.year, next_sem.semester)
    if mod_data_html is None:
        print(f"Failed to fetch mods data for {next_sem}, no new data available")
        exit(1)
    print(f"Success! Fetched mods data for {next_sem}")
    progress_semester(MODS_KEY)
    print(f"Progressed to {next_sem}")