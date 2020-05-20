# Launch Guide

### Backend

#### Prerequisite

1. MySQL database on `localhost:3306` with account username `root` and no password
	> You may change the database settings in [backend/backend/settings.py L82~84](backend/backend/settings.py)

2. Python 3.8

#### To launch a brand new project

0. The following steps are for launching a brand new project. If you have the initial data `tcas_demo.sql`, please see the below section: **To start with initial data**.

1. Open a new terminal and locate to the `backend` dir

2. Setup and activate Python3 virtual environment (recommended)
	In Windows:
	```sh
	python -m venv venv
	venv\Scripts\activate
	```

3. Install required packages
	```sh
	pip install -r < requirements.txt
	```

4. Manually create a database `tcas` in MySQL using account "root"
	```sql
	create database tcas;
	```

5. Run Django migration command to initialize database structure
	```sh
	python manage.py migrate
	```

6. Create a teacher account
	```
	python manage.py createsuperuser
	```

	then follow the instructions.

7. Run the server for testing
	```
	python manage.py runserver 8008
	```

#### To start with initial data

1. Open a new terminal and locate to the `backend` dir

2. Setup and activate Python3 virtual environment (recommended)
	In Windows:
	```sh
	python -m venv venv
	venv\Scripts\activate
	```

3. Install required packages
	```sh
	pip install -r < requirements.txt
	```

4. Import the sql file into your MySQL database

5. Startup the server
	```
	python manage.py runserver 8008
	```

### Frontend

#### Prerequisite

1. [Node.js](https://nodejs.org/en/) (LTS version is recommended)

2. [Yarn package manager (classic)](https://classic.yarnpkg.com/en/docs/install)

#### To launch

1. Open a new terminal and locate to the `frontend` dir

2. Install required packages
	```
	yarn
	```

3. Run the serving command
	```
	yarn run serve
	```

4. You will get URLs in the console to access the webpages.
