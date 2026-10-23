# Flask SQLAlchemy Workout Application Backend
## Installation
pipenv install
pipenv shell
## Database Setup
cd server
flask db init
flask db migrate -m "Create tables"
flask db upgrade head
python seed.py
## Run
flask run
