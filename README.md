# Assignment


## Description
Backend system that allows users to manage data schemas, perform CRUD operations, and
handle large data imports efficiently. The system have secure, flexible APIs


## Features
- ✅ Schema Management
- ✅ CRUD Operations with Search
- ✅ Data Import Functionality

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/mazen15/Assignment.git

2. Navigate to the project directory:
3. 
   cd .\assignment\

4. Install dependencies:
   
   python -m venv env
   
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
   
   .\env\Scripts\Activate.ps1
   
   pip install Django
   
   pip install djangorestframework
   
   pip install psycopg2-binary
   
   pip install djangorestframework-simplejwt
   
   pip install celery
   
   pip install redis
   

5. Start Redis
   
   redis-server --port 6381

6. Start Celery:
   
   celery -A assignment.celery worker --loglevel=info --pool=solo

7. Run the Project
   
   python manage.py runserver

API Endpoints
Method	Endpoint	Description
1. GET	/api/token/	Return the Token that will be used in the API followed next use username and password in the Body with the admin user credentials
2. POST	assignmentapp/api/table/create-table/	Api to create a new table using the generated token in the header as authorization and a json including the table data in the body
                                    {
                                        "name": "customer",
                                        "fields": [
                                            {"name": "name", "field_type": "text"},
                                            {"name": "email", "field_type": "text", "is_unique": true},
                                            {"name": "created_at", "field_type": "date"}
                                            ]
                                    }
3. POST	assignmentapp/api/table/edit-table/	Api to edit a table using the generated token in the header as authorization and a json including the table data in the body
                                    {
                                           "name": "customer",
                                          "add_fields": [{"name": "phone_number", "field_type": "text"}],
                                          "remove_fields": ["email"]
                                    }

4. Delete /assignmentapp/api/table/delete-table/ Api to delete a table using the generated token in the header as authorization and a json including the table data in the body
                                 {
                                   "name": "customer"
                                 }
