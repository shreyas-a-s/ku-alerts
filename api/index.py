import json

import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)


def extract_tables(url):
    # Fetch webpage content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Define substring to search for
    search_text = "B.Tech"

    # Find all <tr> elements that contain a <td> with the substring "Fruit"
    matching_rows = [
        tr
        for tr in soup.find_all("tr")
        if any(search_text in td.text for td in tr.find_all("td"))
    ]

    return matching_rows


# Example Usage
url = "https://exams.keralauniversity.ac.in/Login/check1"
tables_data = extract_tables(url)

data = []

for tr in tables_data:
    tds = tr.find_all("td")  # Get all <td> elements

    if (
        len(tds) >= 2
    ):  # Ensure there are at least 2 <td> elements (description and link)
        description = tds[1].get_text(strip=True)  # Extract text from the second <td>
        link_tag = tds[2].find("a")  # Find <a> inside the last <td>
        pdf_link = link_tag["href"] if link_tag else None  # Extract href from <a>

        data.append({"description": description, "pdf_link": pdf_link})

# Convert to JSON string (optional)
json_data = json.dumps(data, indent=4)


@app.route("/")
def index():
    return render_template("table.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)

