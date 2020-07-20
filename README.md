FlaskUser
---------

An API template written in Flask with user authentication, session management using Redis,
and Client and Project management functionality built in. Project uses 
User authentication implemented with sessions and additional example user functionality
is added.

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
```
> virtuanenv venv
> source env/bin/activate
```

#### (ii) Install requirements and set environment variables
```
> pip install -r requirements.txt
> export FLASK_ENV=development
> export FLASK_APP=run.py
```

#### (iii) Run tests
`> python -m pytest tests/`

#### (v) Run application
`> python -m flask run`


#### Additional Notes:
This application requires PostgreSQL
