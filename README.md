python3 -m venv ckg
source ckg/bin/activate

pip install django

django-admin startproject blog_main

python3 manage.py runserver

python3 manage.py migrate

python3 manage.py createsuperuser

# https://www.toptal.com/developers/gitignore 

