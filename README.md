# Project Null-Void

Hello World! Checkout my django App deployed on [Heroku](https://null-void.herokuapp.com/).

--------------------------------------------------

The steps to deploy are mentioned below.
----------------------------------------

1. Create a project and push it to github.

2. Make a new area of the codebase by cloning from github and do a git init.

3. create a requirements.txt for the project using pip freeze > requirements.txt
Ideally, install these packages:
```bash
dj-database-url==0.4.1
Django==1.11.1
gunicorn==19.6.0
psycopg2==2.6.2
whitenoise==3.2
datefinder==0.6.1
python-dateutil==2.6.1
django-extensions==1.9.7
```

4. create a file called "Procfile" and enter this line: 
```text
web: gunicorn myproject.wsgi --log-file -
```

5. Makes changes to settings.py and wsgi.py according to the config described in this link: 
https://devcenter.heroku.com/articles/django-app-configuration

6. Run locally to test it: 
 ```bash
 heroku local web
```

7. If you do not have an account in heroku, follow the procedure [here](https://devcenter.heroku.com/articles/heroku-cli) to install heroku.

8. Create a new app in Heroku from the web interface. You'll get instructions on how to deploy your app. Follow the steps given below if required.

9. After login to Heroku and following all the above steps till here. Run this command after a git init in the cloned area. 
```bash
heroku git:remote -a app-name
git add .
git commit -am "make it better"
git push heroku master
```

10. Go to the web app console on heroku.com and do the following if it's a django app:
```bash
./manage migrate
./manage createsuperuser
```

--------------------------------------------------

##### This project started from following tutorial on djangogirls.com

Checkout the tutorial from here https://tutorial.djangogirls.org/en/

Also deployed code on http://pyprat1.pythonanywhere.com/

--------------------------------------------------
