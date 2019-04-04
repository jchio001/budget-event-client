# Preface

I've made several comments about how anyone with access to Google search and Heroku can build a basic events platform, 
so here's a rudimentary implementation of an events logging platform. All it does is push events to Google Analytics 
and prevent duplicate events from being logged to Google Analytics. It can handle pushing a single event, or pushing 
multiple events if you're a big fan of minimizing networking resources.

I would <b>not</b> recommend using this for any serious application development.

## Running locally

Please ensure that the following tools are installed on your laptop:
- Python 2.7 (NOTE: Python 2.7 is the default on Mac!
- virtualenv (This should be done after installing Python3! Virtualenvs allows us to isolate python dependencies for a 
project, meaning that we have multiple projects cleanly running multiple different versions of a library. [Here's a 
good guide on installing and setting up a virtualenv.](
https://packaging.python.org/guides/installing-using-pip-and-virtualenv/))  

Once the Python environment has been set up correctly and that there's a virtualenv up and running, download all the 
requirements contained in `requirements.txt` with:
```bash
pip install -r requirements.txt
```

You can then boot up the application locally by running:
```bash
gunicorn -w 2 -b 0.0.0.0:<YOUR PORT HERE> routes:app
```

## Deploying onto Heroku

All you need to do to deploy is to press this button:

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jchio001/budget-event-client)

Once this application is deployed, 2 environment variables need to be set:
`events_db_url`: a URI to the database which data will be pushed into. If you don't have your own database/don't want to 
go through the trouble of starting one up, Heroku's `Heroku Postgres` add on can boot one up fairy quickly.
`event_tracking_id`: The id of your application on Google Analytics

