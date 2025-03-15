import requests
from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template

app = Flask(__name__)

url = "https://exams.keralauniversity.ac.in/Login/check1"
course_map = {
    "bsc": "B.Sc",
    "bdes": "B.Des",
    "bped": "B.P.Ed",
    "bvoc": "B.Voc",
    "ba": "B.A",
    "barch": "B.Arch",
    "bba": "BBA",
    "bca": "BCA",
    "bcom": "B.Com",
    "bed": "B.Ed",
    "bfa": "BFA",
    "bhm": "BHM",
    "bhmct": "BHMCT",
    "bms": "BMS",
    "bpa": "BPA",
    "bpes": "BPES",
    "bsw": "BSW",
    "btech": "B.Tech",
    "llb": "LL.B",
    "llm": "LLM",
    "mdes": "M.Des",
    "med": "M.Ed",
    "ma": "M.A",
    "march": "M.Arch",
    "mba": "MBA",
    "mca": "MCA",
    "mcj": "MCJ",
    "mcom": "M.Com",
    "mfa": "MFA",
    "mliblsc": "MLiblSc",
    "mlisc": "MLISc",
    "mpa": "MPA",
    "mped": "M.P.Ed",
    "mpes": "MPES",
    "mplan": "MPlan",
    "msc": "M.Sc",
    "msw": "MSW",
    "mta": "MTA",
    "mtech": "M.Tech",
    "mttm": "MTTM",
    "mva": "MVA",
}


def convert_course_string(course):
    if course.lower() in course_map:
        return course_map[course.lower()]

    return ""


def extract_rows(url):
    # Fetch webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Find all the tr inside the div with id 'wrapper'
    tr_list = soup.find("div", id="wrapper").find_all("tr")

    return tr_list


def search_course(tr_list, course=""):

    # Find all <tr> elements that either contain the substring "course" or have a class of "tableHeading"
    matching_rows = [
        tr
        for tr in tr_list
        if (
            tr.get("class")
            and (
                any(course in td.text for td in tr.find_all("td"))
                or "tableHeading" in tr.get("class")
            )
        )
    ]

    return matching_rows


def extract_semester_num(description):
    number_map = {
        "first": 1,
        "second": 2,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10,
    }

    normalized_description = description.lower().replace(" ", "")
    found_numbers = [
        str(number_map[key])
        for key in number_map
        if f"{key}semester" in normalized_description
        or f"{key}and" in normalized_description
    ]

    return ",".join(found_numbers) if found_numbers else "-"


def process_data(tables_data):
    final_variable = []
    current_published_date = None
    notifications = []

    for tr in tables_data:
        # Check if the row is a table heading (contains the published date)
        if "tableHeading" in tr.get("class", []):
            # If there is an existing group of notifications, save them
            if current_published_date:
                final_variable.append(
                    {
                        "published_date": current_published_date,
                        "published_year": current_published_year,
                        "notifications": notifications,
                    }
                )

            # Extract the published date from the first <td>
            published_date = tr.find("td").get_text(strip=True).split()[2]
            published_date = published_date[:-5]
            published_year = f"/{published_date[-2:]}"
            current_published_date = published_date
            current_published_year = published_year
            notifications = []  # Reset the notifications for the new published date
        else:
            # Process rows with notification data
            tds = tr.find_all("td")

            # For rows with just one <td> (description only)
            if len(tds) == 1:
                description = tds[0].get_text(strip=True)
                semester_num = extract_semester_num(description)
                notifications.append(
                    {
                        "description": description,
                        "semester_num": semester_num,
                        "pdf_link": None,
                    }
                )
            elif (
                len(tds) >= 2
            ):  # For rows with at least two <td> elements (description and pdf link)
                description = tds[1].get_text(strip=True)
                semester_num = extract_semester_num(description)
                link_tag = tds[2].find("a")  # Find <a> inside the last <td>
                pdf_link = link_tag["href"] if link_tag else None
                notifications.append(
                    {
                        "description": description,
                        "semester_num": semester_num,
                        "pdf_link": pdf_link,
                    }
                )

    # Don't forget to append the last set of notifications after the loop
    if current_published_date:
        final_variable.append(
            {"published_date": current_published_date, "notifications": notifications}
        )

    return final_variable


tables_rows = extract_rows(url)
course_data = search_course(tables_rows, "")
processed_course_data = process_data(course_data)


@app.route("/")
def index():
    # Check if at least one entry has a non-empty 'notifications'
    has_notifications = any(item.get("notifications") for item in processed_course_data)

    return render_template(
        "table.html",
        data=processed_course_data,
        course="all",
        course_map=course_map,
        has_notifications=has_notifications,
    )


@app.route("/course/<course>")
def show_course_notifications(course):
    course_string = convert_course_string(course)
    course_data = search_course(tables_rows, course_string)
    processed_course_data = process_data(course_data)

    # Check if at least one entry has a non-empty 'notifications'
    has_notifications = any(item.get("notifications") for item in processed_course_data)

    return render_template(
        "table.html",
        data=processed_course_data,
        course=course,
        course_map=course_map,
        has_notifications=has_notifications,
    )


@app.route("/course/")
def no_course_redirect():
    return redirect("/course/all")


if __name__ == "__main__":
    app.run()
