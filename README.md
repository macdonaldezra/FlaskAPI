FlaskUser v1.0
--------------

A minimal API for creating, updating, and deleting user accounts using Flask.

User authentication is implemented using sessions, alternative to Flask's default
client-side cookie implementation. Additional example functionality is added for
managing a User's clients.


Project Structure
-----------------

```bash
├── app
│   ├── main
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── view.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── test_clients.py
│   │   ├── test_user.py
│   ├── __init__.py
│   ├── migrations
│   ├── auth.py
│   ├── config.py
│   ├── custom_form.py
│   ├── models.py
│   ├── requirements.txt
│   └── run.py
└── .gitignore
```

##### main:
Contains API endpoint files including views for logical procesing and forms for validation.


#### Recommended structure for additional API modules:
```bash
├── app
│   ├── new_module
│   │   ├── __init__.py
│   │   ├── forms.py
│   │   ├── view.py
   ....
```


Installation & Testing
-------------------------

#### (i) Create & activate a Python v3.6+ virtual environment
python -m venv ./env/
source env/bin/activate

#### (ii) Install requirements and set environment variables
pip install -r requirements.txt
export FLASK_ENV=development

#### (iii) Run tests
python -m pytest tests/

#### (iv) Run test coverage
pip install coverage
coverage run -m ptest tests/
coverage report -m *.py main/*.py

#### Additional Notes:
This application requires PostrgreSQL

Current Test Coverage Results
-----------------------------

|  Name | Statements  | Miss  | Cover  | Missing  |
|  ------------  | ------------ | ------------ | ------------ | ------------ |
| auth.py  | 18  | 2  | 89%  | 17, 20  |
| config.py  | 26  | 0  | 100%  |   |
| custom_forms.py  | 16  | 1  | 94%  | 26  |
| models.py  | 173  | 68  | 61%  | 38, 67, ... , 270 |
|  run.py | 18  | 2  | 89%  | 24-25  |
| main/forms.py | 24  | 0  | 100%  |   |
|  main/views.py | 194  | 49  | 75%  | 35-36, 52, ... , 252 |
|  ------------  | ------------ | ------------ | ------------ | ------------ |
|  TOTAL | 469  | 122  | 74%  | ------------ |
