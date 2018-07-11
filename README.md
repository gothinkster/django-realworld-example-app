# ![Django DRF Example App](project-logo.png)

> ### Example Django DRF codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld-example-apps) API spec.

<a href="https://thinkster.io/tutorials/django-json-api" target="_blank"><img width="454" src="https://raw.githubusercontent.com/gothinkster/realworld/master/media/learn-btn-hr.png" /></a>

This repo is functionality complete — PR's and issues welcome!


## Prerequisites

* Python 3.4+
* Git
* Shell prompt ([Git BASH for windows](https://gitforwindows.org/) recommended for windows)


## Installation

1. Clone this repository: `git clone git@github.com:gothinkster/django-realworld-example-app.git`.
2. `cd` into `django-realworld-example-app`.
3. Create a new virtualenv `python -m venv venv/`
4. Install requirements `venv/bin/pip install -r requirements.txt`
5. Create database `venv/bin/python manage.py migrate`
6. Create superuser `venv/bin/python manage.py createsuperuser`
7. Run dev server `venv/bin/python manage.py runserver 0.0.0.0:4000`


#### Notes

* `python` should be Python 3.4+, check using `python --version`. To be explicit, if on Linux/MacOS you may have a `python3.5` or `python3.6` on your path.
* If using windows use `venv\Scripts\python` instead of `venv/bin/python`
