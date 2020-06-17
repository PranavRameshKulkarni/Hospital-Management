The following instructions are for installation of HOSPITAL MANAGEMENT APP in Windows 10 environment

1. Download the zip file and unzip it in required location.
2. Start the virtual environment with the command 
	python -m venv venv_name
3. Activate venv with the command 
	.\venv_name\Scripts\activate
4.Install all requirements from the file requirements.txt with command
	pip install -r requirements.txt
5.Migrate all the tables in the sqlite database with the commands
	python manage.py makemigrations
	python manage.py migrate
6.Run the server with
	python manage.py runserver
Hope this command will run the app.

7.Terminate the server to create super user for the database access
	python manage.py createsuperuser

8.Register the patients using register menu and traverse through the app

