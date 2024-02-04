# Catalyst_count

This is a project that have user creation and data upload operations.

## Installation

1. Clone the repository: `git clone https://github.com/rajesh80879/catalyst.git`
2. Create a python env and activate 
3. Install dependencies: `pip install -r requirements.txt`
4. make migration:  `python manage.py makemigrations user record`
5. migrate:  `python manage.py migrate`
6. create superuser: `python manage.py createsuperuser`
7. run the project:  `python manage.py runserver`

## Database and env setup

-Create an .env in catalyst_count folder

-Add the following configuration variables to the `.env` file:

    SECRET_KEY='your-secret-key'
    DEBUG=True
    ALLOWED_HOSTS=*
    DATABASE_ENGINE=django.db.backends.postgresql

    DATABASE_NAME='your-database-name'
    DATABASE_USER='db-user'
    DATABASE_PASSWORD='db-password'
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
