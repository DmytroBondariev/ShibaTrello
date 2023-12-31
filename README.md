# IT-Company-Task-Manager

This project is a task manager with a list of associates and the ability to create/bind tasks

## Getting Started

[IT Company Task Manager Deployed to Render](https://it-company-task-manager-xbod.onrender.com/)

Login credentials
```
username: user
password: Password12345
```
Enjoy testing service functionality!
### Prerequisites

Python3 must be installed!

```
pip install python3
```

### Installing

Follow next steps:

```shell
git clone https://github.com/Dmytry95/IT-Company-Task-Manager.git
cd it_company_task_manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```


## Running the tests
```
python manage.py test
```

Run that command to make tests for models, admin page and views.


## Environment Variables

The project uses environment variables for configuration. Create a `.env` file in the project directory and define the following variables:

You can use the `.env.sample` file provided as a template:

1. Rename the `.env.sample` file to `.env`.
2. Fill `DJANGO_SECRET_KEY` with your actual Django secret key.

Make sure not to commit the `.env` file to version control.




## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Creative Tim](https://www.creative-tim.com/) - The web framework used
* [Ira Design](https://iradesign.io/) - Illustrations


## Authors

* **Dmytro Bondariev** - *Initial work* - [GitHub](https://github.com/Dmytry95)
