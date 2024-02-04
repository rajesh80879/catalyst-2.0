# Catalyst_count 2.0

This is a project that has user creation and data upload operations.

## Installation

1. Clone the repository: `git clone https://github.com/rajesh80879/catalyst.git`
2. Create a python env and activate 
3. Install dependencies: `pip install -r requirements.txt`
4. Make migration:  `python manage.py makemigrations user record`
5. Migrate:  `python manage.py migrate`
6. Create superuser: `python manage.py createsuperuser`
7. Run the project:  `python manage.py runserver`

## Database and env setup

- Create an `.env` file in the `catalyst_count` folder.

- Add the following configuration variables to the `.env` file:

    ```plaintext
    SECRET_KEY=django-insecure-bp$owpv1yj4g1#pg3u^(kp#&qxm(-4+&kpv#0co0-)5k@&bv70
    DEBUG=True
    ALLOWED_HOSTS=*


    DATABASE_ENGINE=django.db.backends.postgresql
    DATABASE_NAME='your-database-name'
    DATABASE_USER='db-user'
    DATABASE_PASSWORD='db-password'
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```

- Alternatively, you can use SQLite as the database. Uncomment the following configuration in the `settings.py` file:

    ```python
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
    ```


### Functionalities

### 1. Data Upload Page

- **Description**: This page allows users to upload data to the system.
- **Features**:
- File upload form.
- Processing and storing uploaded data.
- Response messages for successful uploads or errors.


### 2. Data Filtering Page

- **Description**: This page allows users to filter the uploaded data based on certain criteria.
- **Features**:
- Filter options for different fields (e.g., industry, year founded, location).
- Display of filtered data.
- Count of the data from an api using drf

### 3. User Management Page

- **Description**: This page allows administrators to manage user accounts within the system.
- **Features**:
- User listing with basic details (e.g., username, email).
- Options to add or delete user accounts.

### Additional Considerations

- **Authentication**: User authentication is implemented to control access to different pages and functionalities.
- **Error Handling**: Errors or invalid inputs are handled in each functionality to provide a smooth user experience.

Note: Choose either PostgreSQL or SQLite as your database backend.
