user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

current_year = 2025
current_semester = 1

next_year = 2025
next_semester = 2

def progress_semester():
    global current_year, current_semester, next_year, next_semester
    current_year = next_year
    current_semester = next_semester
    if current_semester == 2:
        next_year += 1
        next_semester = 1
    else:
        next_semester += 1
