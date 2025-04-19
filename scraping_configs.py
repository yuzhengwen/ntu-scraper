import json
from enum import Enum

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

class semester:
    def __init__(self, year, semester):
        self.year = year
        self.semester = semester

    def __str__(self):
        return f"{self.year} Semester {self.semester}"

    def __repr__(self):
        return str(self)
    
    def next(self):
        if self.semester == 2:
            return semester(self.year + 1, 1)
        else:
            return semester(self.year, 2)
    def set_next(self):
        next_sem = self.next()
        self.year = next_sem.year
        self.semester = next_sem.semester

EXAM_KEY = "latest_exam_sem"
MODS_KEY = "latest_mod_sem"

def get_latest_semester(key):
    with open("latest.json", "r") as f:
        data = json.load(f)
        if key not in data:
            raise KeyError(f"{key} not found in latest.json")
        return semester(data[key]["year"], data[key]["semester"])

def progress_semester(key):
    with open("latest.json", "r") as f:
        data = json.load(f)
        if key not in data:
            raise KeyError(f"{key} not found in latest.json")
        current_sem = semester(data[key]["year"], data[key]["semester"])
        current_sem.set_next()
        data[key]["year"] = current_sem.year
        data[key]["semester"] = current_sem.semester
    with open("latest.json", "w") as f:
        f.write(response := json.dumps(data, indent=4))
# with open("latest.json", "w") as f:
#     f.write(response := json.dumps(latest, default=lambda o: o.__dict__, indent=4))

