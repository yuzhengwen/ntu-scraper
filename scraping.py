import requests, os
from scraping_configs import user_agent

url = "https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"

def fetch_data(academic_year="2025", semester="1", save_path="data.html"):
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
    
    print("Data fetched successfully")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    print("Saving data to", save_path)
    with open(save_path, "w") as f:
        f.write(response.text)
    print("Data saved")
    return response.text
