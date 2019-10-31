# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, create and restore a database using the `trivia.psql` file provided.
- *NOTE* You will need to edit the `OWNER` in the `trivia.psql` file to the name of the database user.
    For instance `ALTER TABLE public.categories OWNER TO [DATABASE_USERNAME];`. Do this for all such instances in the file.
From the backend folder in terminal run: 
```bash
createdb trivia
psql trivia < trivia.psql
```
Create another database that will be used for running tests.
```bash
createdb trivia_test
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

- Create a `.env` file in the root of the `backend` directory. 
- Copy the contents of `.env.example` into the `.env` file and edit with the database information from the previous section
- Run the tests `python test_flaskr.py`. If the tests all pass, then the setup was successfull.
- Run the application on `http://localhost:5000`

```bash
source .env
flask run
```

## Testing
To run the tests, run
```
python test_flaskr.py
```
## API Documentation.
The documentation for the Trivia API are available at in the [docs/APIDOCS.md](docs/APIDOCS.md) file.
