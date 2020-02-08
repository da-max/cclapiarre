# CC La Piarre



This site is online on : https://cclapiarre.deblan.fr

The but of this site is to help the operation of the *court-circuit buëch* organisation.



## Requirements

* Python 3.5 (or later)

* Pip

* Npm

* Venv

* Git



## How to build



It is recommended to create a python's venv before install requirements with this command and activate this venv :

`python -m venv <path_to_venv>`

`source <path_to_venv>/bin/activate`

Then, clone the repository :

`git clone https://gitlab.com/Da-max/cclapiarre`

Go to the folder and install requirements.txt with :

`pip install -r ./requirements.txt`



Makemigrations and migrate with :

`python ./manage.py makemigrations && python ./manage.py migrate`



Then go to the `frontend` folder and run :

`npm i` for install npm install

You can start the project with, in the frontend folder :

`npm run serve`

and on the root of the project :

`python ./manage.py runserver`

**Warning, you must first launched npm then django.** 



You can also, create super user with : `python ./manage.py createsuperuser` then inquire username, email and password.










