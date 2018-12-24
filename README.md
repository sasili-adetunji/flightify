# flightify
flightify is flight booking automation application.

### Features of Fightify
- Registration POST `api/v1/accounts/signup/`
- Activate an account `POST api/v1/accounts/activate/<activate_key>/`
- Login POST `api/v1/auth/token/`
- Upload a profile picture POST `api/v1/uploads/`
- Update profile picture PUT `api/v1/uploads/<upload_id>/`
- Delete profile picture DELETE `api/v1/uploads/<upload_id/`
- Retrieve a profile picture GET `api/v1/uploads/<upload_id/`
- Flight reservation POST `api/v1/flights/`
- Get all Flight reservation GET `api/v1/flights/`
- Retrive a single reserved flight GET `api/v1/flights/<flight_id>/`
- Update reserved flight PUT `api/v1/flights/<flight_id>/`
- List and count all users for flight on a specific day GET `api/v1/flights/users/{day(yyyy-mm-day)/`
- Check the status of flight `api/v1/tickets/status/<flight_id>`
- Book Ticket POST `api/v1/tickets/`
- Receive tickets as an email when a flight is booked
- Recieve a reminder email when a flight is due in 24hours


### Installation Guide
- Clone this repository with "git clone https://github.com/sasili-adetunji/flightify.git"
- run `cd flightify`
- Install Virtual environement by running `pip install virtualenv`. This helps in isolating python packages from every project. This makes projects with conflicting dependecies to coeexist peacefully
- Create a vitual env by running `python3 -m venv`
- Activate virtual environment `source venv/bin/activate`
- Edit the `.env.sample` file and save it as `.env` 
- Install the dependencies by running `pip install -r requirements.txt`
- Start the app by running `python manage.py runserver`
- Run test by running `python ../manage.py test`
- Navigate to `localhost:8000`

### Technologies
- Python3: An interpreted, open source programming language with a focus on simplicity and readability.

- Django: Django is a free and open source, python-based software web application library which follows the MVT appraoch (Model View Template) released in 2005. It encourages rapid development of application.

- Postgres: PostgreSQL, often simply Postgres, is an object-relational database management system (ORDBMS) with an emphasis on extensibility and standards compliance. As a database server, its primary functions are to store data securely and return that data in response to requests from other software applications.

### License
This project is authored by Sasiliyu Adetunji, and is licensed for use, distribution and modification under the MIT license