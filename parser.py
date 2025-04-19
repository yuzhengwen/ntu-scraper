from bs4 import BeautifulSoup
import json
import os
import shutil

def parse_data(data_file, save_folder="data"):
    mods = []
    with open(data_file) as f:
        soup = BeautifulSoup(f, "html.parser")

        # extract code, name, aus by matching table width and font color
        course_names = []
        for td in soup.find_all("td", width="500"):
            font = td.find('font', {'color': '#0000FF'})
            if font:
                course_names.append(font.text.strip())

        course_codes = []
        for td in soup.find_all("td", width="100"):
            font = td.find('font', {'color': '#0000FF'})
            if font:
                course_codes.append(font.text.strip())

        aus = []
        for td in soup.find_all("td", width="50"):
            font = td.find('font', {'color': '#0000FF'})  
            if font:
                aus.append(font.text.strip())

        tables = soup.find_all("table", border="")  
        for i, table in enumerate(tables):
            course_code = course_codes[i]
            course_name = course_names[i]
            academic_units = float(aus[i].replace(" AU", ""))
                
            rows = tables[i].find_all("tr")[1:]  # Skip first row (table header)

            indexes = []
            for row in rows:
                cells = row.find_all("td")
                index = cells[0].text.strip()
                lesson_type = cells[1].text.strip()
                group = cells[2].text.strip()
                day = cells[3].text.strip()
                time = cells[4].text.strip()
                venue = cells[5].text.strip()
                remark = cells[6].text.strip()

                if index:
                    indexes.append({
                        "index": index,
                        "lessons": []
                    })
                indexes[-1]["lessons"].append({
                    "lesson_type": lesson_type,
                    "group": group,
                    "day": day,
                    "time": time,
                    "venue": venue,
                    "remark": remark,
                })

            course_document = {
                "course_code": course_code,
                "course_name": course_name,
                "academic_units": academic_units,
                "indexes": indexes
            }
            mods.append(course_document)
            print(f"Added {course_code} {course_name}")


    if (os.path.exists(save_folder)):
        print("Deleting old data folder")
        shutil.rmtree(save_folder)
    print("Creating new data folder")
    os.makedirs(save_folder)

    print("Creating full data file")
    out_file = open(save_folder+"/module_full_data.json", "w")
    json.dump(mods, out_file)
    out_file.close()

    print("Creating module list file")
    out_file = open(save_folder+"/module_list.json", "w")
    json.dump([{"course_code": mod["course_code"], "course_name": mod["course_name"], "aus": mod['academic_units']} for mod in mods], out_file)
    out_file.close()

    print("Creating individual module files")
    os.makedirs(save_folder+"/mods")
    for mod in mods:
        out_file = open(f"{save_folder}/mods/{mod['course_code']}.json", "w")
        json.dump(mod, out_file)
        out_file.close()

    #db.insert_many(mods)