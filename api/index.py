from urllib.request import urlopen

from bottle import Bottle, redirect, static_file, template
from selectolax.parser import HTMLParser

course_map = {
    "all": {"title": "All Courses", "keywords": [""]},
    "bsc": {"title": "B.Sc", "keywords": ["B.Sc"]},
    "bdes": {"title": "B.Des", "keywords": ["B.Des"]},
    "bped": {"title": "B.P.Ed", "keywords": ["B.P.Ed"]},
    "bvoc": {"title": "B.Voc", "keywords": ["B.Voc"]},
    "ba": {"title": "B.A.", "keywords": ["B.A."]},
    "barch": {"title": "B.Arch", "keywords": ["B.Arch"]},
    "bba": {"title": "BBA", "keywords": ["BBA"]},
    "bca": {"title": "BCA", "keywords": ["BCA"]},
    "bcom": {"title": "B.Com", "keywords": ["B.Com"]},
    "bed": {"title": "B.Ed", "keywords": ["B.Ed"]},
    "bfa": {"title": "BFA", "keywords": ["BFA"]},
    "bhm": {"title": "BHM", "keywords": ["BHM"]},
    "bhmct": {"title": "BHMCT", "keywords": ["BHMCT"]},
    "bms": {"title": "BMS", "keywords": ["BMS"]},
    "bpa": {"title": "BPA", "keywords": ["BPA"]},
    "bpes": {"title": "BPES", "keywords": ["BPES"]},
    "bsw": {"title": "BSW", "keywords": ["BSW"]},
    "btech": {"title": "B.Tech", "keywords": ["B.Tech"]},
    "llb": {"title": "LL.B", "keywords": ["LLB", "LL.B"]},
    "llm": {"title": "LLM", "keywords": ["LLM", "LL.M"]},
    "mdes": {"title": "M.Des", "keywords": ["M.Des"]},
    "med": {"title": "M.Ed", "keywords": ["M.Ed"]},
    "ma": {"title": "M.A.", "keywords": ["M.A."]},
    "march": {"title": "M.Arch", "keywords": ["M.Arch"]},
    "mba": {"title": "MBA", "keywords": ["MBA"]},
    "mca": {"title": "MCA", "keywords": ["MCA"]},
    "mcj": {"title": "MCJ", "keywords": ["MCJ"]},
    "mcom": {"title": "M.Com", "keywords": ["M.Com"]},
    "mfa": {"title": "MFA", "keywords": ["MFA"]},
    "mliblsc": {"title": "MLiblSc", "keywords": ["MLiblSc"]},
    "mlisc": {"title": "MLISc", "keywords": ["MLISc"]},
    "mpa": {"title": "MPA", "keywords": ["MPA"]},
    "mped": {"title": "M.P.Ed", "keywords": ["M.P.Ed"]},
    "mpes": {"title": "MPES", "keywords": ["MPES"]},
    "mplan": {"title": "MPlan", "keywords": ["MPlan"]},
    "msc": {"title": "M.Sc", "keywords": ["M.Sc"]},
    "msw": {"title": "MSW", "keywords": ["MSW"]},
    "mta": {"title": "MTA", "keywords": ["MTA"]},
    "mtech": {"title": "M.Tech", "keywords": ["M.Tech"]},
    "mttm": {"title": "MTTM", "keywords": ["MTTM"]},
    "mva": {"title": "MVA", "keywords": ["MVA"]},
}


def convert_course_keywords(course):
    if course.lower() in course_map:
        return course_map[course.lower()]["keywords"]

    return [""]


def extract_rows(url):
    # Fetch webpage content
    html = urlopen(url).read().decode("utf-8")

    # Parse HTML with selectolax
    tree = HTMLParser(html)

    # Find all <tr> elements inside <div id="wrapper">
    tr_list = tree.css("div#wrapper tr")

    # Extract text from each row
    rows = [tr for tr in tr_list]

    return rows  # Returns a list of row text contents


def search_course(tr_list, course_keywords=[]):
    # Find all <tr> elements that either contain the any of the course keywords or have a class of "tableHeading"
    matching_rows = [
        tr
        for tr in tr_list
        if (
            tr.attributes.get("class")
            and (
                any(
                    any(keyword in td.text() for keyword in course_keywords)
                    for td in tr.css("td")
                )
                or "tableHeading" in tr.attributes.get("class")
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
        if "tableHeading" in tr.attributes.get("class"):
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
            published_date_full = tr.css("td")[0].text().split()[2]
            published_date = published_date_full[:-5]
            published_year = f"/{published_date_full[-2:]}"
            current_published_date = published_date
            current_published_year = published_year
            notifications = []  # Reset the notifications for the new published date
        else:
            # Process rows with notification data
            tds = tr.css("td")

            # For rows with just one <td> (description only)
            if len(tds) == 1:
                description = tds[0].text()
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
                description = tds[1].text()
                semester_num = extract_semester_num(description)
                link_tag = tds[2].css("a")  # Find <a> inside the last <td>
                pdf_link = link_tag[0].attributes.get("href") if link_tag else None
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
            {
                "published_date": current_published_date,
                "published_year": current_published_year,
                "notifications": notifications,
            }
        )

    return final_variable


def get_course_data(course):
    course_keywords = convert_course_keywords(course) if course else [""]
    course_data = search_course(tables_rows, course_keywords)
    return process_data(course_data)


app = Bottle()
TEMPLATE_PATH = "api/templates/table.html"
STATIC_PATH = "api/static"
url = "https://exams.keralauniversity.ac.in/Login/check1"
tables_rows = extract_rows(url)


@app.route("/")
def index():
    return show_course_notifications("all")  # Reuse the route


@app.route("/course/<course>")
def show_course_notifications(course):
    processed_course_data = get_course_data(course)

    return template(
        TEMPLATE_PATH,
        data=processed_course_data,
        course=course,
        course_map=course_map,
        has_notifications=any(
            item.get("notifications") for item in processed_course_data
        ),
    )


for route in ["/course", "/course/"]:
    app.route(route)(lambda: redirect("/course/all"))


@app.route("/static/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=STATIC_PATH)


if __name__ == "__main__":
    app.run()
