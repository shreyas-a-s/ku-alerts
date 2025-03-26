# Kerala University Alerts

This is a project aimed at simplifying the notification-viewing experience of **Kerala University students**.

This is a website that runs using [Bottle.py](https://github.com/bottlepy/bottle) on **Vercel** with **Serverless Functions** using the [Python Runtime](https://vercel.com/docs/concepts/functions/serverless-functions/runtimes/python) 🐍. It can also be run locally for testing and checking it out.

## How it Works

The frontend is built with [React](https://react.dev/) and utilizes [React Router](https://reactrouter.com/) for managing page navigation.

In backend, it scrapes the University webpages using [selectolax](https://github.com/rushter/selectolax) 🕸️, which is a python library that enables easy scraping of html webpages, just like [soup](https://pypi.org/project/beautifulsoup4/)  🍜 which you might know.

It parses the table of notifications 📜 to find the latest ones that contain the `course` string and it lists them using a neat-looking table which also contains a link to download each of those notifications  📎.

For hosting this website, I have used the Web Server Gateway Interface (WSGI) with [Bottle.py](https://github.com/bottlepy/bottle)  to enable handling requests on Vercel with **Serverless Functions** ☁️. This means I am able to run backend code (**python**) *without* the need for a server, which is pretty cool 🚀.

## List of Scraped Web Pages

1. **Notifications** Page - https://exams.keralauniversity.ac.in/Login/check1
2. **Timetables** Page - https://exams.keralauniversity.ac.in/Login/check3
3. **Exam Results** Page - https://exams.keralauniversity.ac.in/Login/check8

## Running Locally

```bash
# Install react dependencies
npm install

# Install python dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run frontend and backend separately
npm run dev
python3 api/index.py

# (or) Run both simultaneously
npm run dev & python3 api/index.py
```

The website is now available at `http://localhost:8080` (the **port** might be different. Check the terminal window for the correct port number)

## One-Click Deploy an Example App

Deploy an example flask/bottle app using [Vercel](https://vercel.com?utm_source=github&utm_medium=readme&utm_campaign=vercel-examples):

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvercel%2Fexamples%2Ftree%2Fmain%2Fpython%2Fflask3&demo-title=Flask%203%20%2B%20Vercel&demo-description=Use%20Flask%203%20on%20Vercel%20with%20Serverless%20Functions%20using%20the%20Python%20Runtime.&demo-url=https%3A%2F%2Fflask3-python-template.vercel.app%2F&demo-image=https://assets.vercel.com/image/upload/v1669994156/random/flask.png)
