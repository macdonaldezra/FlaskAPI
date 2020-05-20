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

### Install & Run
-----------------
```> python -m venv ./env/
> source env/bin/activate
> python -m pip install -r requirements.txt
> export FLASK_ENV=development
> flask run
```

### Test and show coverage
-------------------------------
```> python -m pytest tests/
> python -m pip install coverage
> coverage run -m ptest tests/
> coverage report -m *.py main/*.py
```


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
