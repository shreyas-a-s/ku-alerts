# Kerala University Notifications

This is a project aimed at simplifying the notification-viewing experience of Kerala University students .

This is a website that runs using Flask 3 on Vercel with Serverless Functions using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python). It can also be run locally for testing ang checking it out.

## How it Works

It scrapes the University website's [notifications](https://exams.keralauniversity.ac.in/Login/check1) page using [soup](https://pypi.org/project/beautifulsoup4/), which is a python library that enables easy scraping of html webpages.

It parses the table of notifications to find the latest notifications that contain the `course` string and it lists them using a neat-looking table which also contains a link to download each of those notifications.

For hosting this website, I have used the Web Server Gateway Interface (WSGI) with Flask to enable handling requests on Vercel with Serverless Functions. This means I am able to run backend code (python) *without* the need for a server, which is pretty cool.

## Running Locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 api/index.py
```

The website is now available at `http://localhost:5000`

## One-Click Deploy

Deploy an example flask app using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)
