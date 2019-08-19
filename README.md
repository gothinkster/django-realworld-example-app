# ![Django DRF Example App](project-logo.png)

> ### Example Django DRF codebase containing real world examples (CRUD, auth, advanced patterns, etc) that adheres to the [RealWorld](https://github.com/gothinkster/realworld-example-apps) API spec.

<a href="https://thinkster.io/tutorials/django-json-api" target="_blank"><img width="454" src="https://raw.githubusercontent.com/gothinkster/realworld/master/media/learn-btn-hr.png" /></a>

This repo is functionality complete — PR's and issues welcome!

## Installation

### Option 1: Install from source

1. Clone this repository: `git clone git@github.com:gothinkster/productionready-django-api.git`.
2. `cd` into `conduit-django`: `cd productionready-django-api`.
3. Install [pyenv](https://github.com/yyuu/pyenv#installation).
4. Install [pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv#installation).
5. Install Python 3.5.2: `pyenv install 3.5.2`.
6. Create a new virtualenv called `productionready`: `pyenv virtualenv 3.5.2 productionready`.
7. Set the local virtualenv to `productionready`: `pyenv local productionready`.
8. Reload the `pyenv` environment: `pyenv rehash`.

If all went well then your command line prompt should now start with `(productionready)`.

If your command line prompt does not start with `(productionready)` at this point, try running `pyenv activate productionready` or `cd ../productionready-django-api`. 

If pyenv is still not working, visit us in the Thinkster Slack channel so we can help you out.

#### Setting up the Database

```bash
python manage.py makemigrations
python manage.py migrate
```

#### Running the DJango App
```
python manage.py runserver 0.0.0.0:8000
```

#### Adding an admin user
However, there aren’t any users for our Django DRF application.
In order to create admin user, we need to access our container to run the createuser command then enter the promoted credentials:
```bash
python manage.py createsuperuser
```


### Option 2: Use Docker

If you don't have yet a running docker installation, install first docker with

```bash
sudo apt-get install docker.io
```

Fetch the repository from docker
```bash
docker pull realworldio/django-drf
```

#### Running the DJango App
Create a folder to mount the source code of the app
```bash
mkdir ~/django_drf_project
```

Run the DJango DRF app via Docker container
```bash
docker run -d -p 8080:8000  -v ~/django_drf_project:/drf_src --name django_drf_app realworldio/django-drf
```

#### Adding an admin user
However, there aren’t any users for our Django DRF application.
In order to create admin user, we need to access our container to run the createuser command:
```bash
docker exec -it django_drf_app /bin/bash
```

To add an admin user, you need to run the following code in your container then enter the promoted credentials:
```bash
python manage.py createsuperuser
```

Afterwards, exit the Docker container running the `exit` command.

