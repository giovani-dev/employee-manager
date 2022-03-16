# employee-manager

This is a basic api that you can register employees for  organisation proupose.

### How to setup?
```console
virtualenv .venv -p python3.9
source .venv/bin/activate
pip install -r requirements.txt
```

### How to run the api?
* Only python
```console
(cd EmployeeManager; python manage.py test)
```
* Gunicorn
```console
(cd EmployeeManager; gunicorn EmployeeManager.wsgi --user www-data --bind 0.0.0.0:8000 --workers 2)
```
* Docker-compose
```console
docker-compose -f docker/docker-compose.yml up --build --force
```

### Where`s the api documentation?
* Here you can see all endpoints and more: https://documenter.getpostman.com/view/11940350/UVsMtQJh

### How can i get the api link and admin panel?
* Here is the api link: https://giovani-employee-manager.herokuapp.com
* Here is the api panel: https://giovani-employee-manager.herokuapp.com/admin