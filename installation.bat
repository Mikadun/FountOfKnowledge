pip install django --user
pip install django-crispy-forms --user
pip install django-tinymce --user
pip install django-pillow --user
pip install django-autocomplete-light --user
cd %cd%
py manage.py makemigrations
py manage.py migrate
py manage.py runserver