## Intro

This project will give an introduction to the adapter design pattern in a django app. It will apply to a couple of different currencies exchange rates providers, so we will see how to unify the access to their data using adapters, since they have a heterogeneus data acces interfaces.
In it, a set of exchange rates will be retrieved from the providers and stored into the app database to be used in later steps.
To start working on it, you can clone the repository locally and follow the steps below.


## Requirements

Since django is a python framework it is necesary to have python installed in your system, it is also necesary to have it installed the python package manager to install the dependencies for this project. It is also advisable to use some kind de virtual environment that allows to isolate the project. The source code is stored in a git repository, so having it installed will also simplify the process.
If you don't have it installed, you can have more information here on how to do it:
 - Python: https://www.python.org/downloads/
 - Virtualenv: https://virtualenvwrapper.readthedocs.io/en/latest/install.html
 - Pip: https://packaging.python.org/guides/installing-using-linux-tools/
 - Git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git


By default, the application runs in the port 8000, so it has to be free to be able to run it


## Quick Start

First step is to clone or download the repository, this can be easily done like this:
```sh
git clone https://github.com/PedroDDiez/django-adapters.git <project-name>
```

After that, you can move into that folder and create the virtual environment, so all the packages and dependencies will apply only to this project. 
```sh
cd <project-name>
mkvirtualenv --python=python3 nucoro_currency
```

Once in the virtual environment, you can now install the requierements. It will download and install all needed packages:
```sh
pip install -r requirements.txt
```

Now the app is installed, so let's set up the database, this will create the database, and also populate the providers and currency tables:
```sh
python manage.py migrate
```

Create a superuser to access the admin site
```sh
python manage.py createsuperuser
```

Run a development server
```sh
python manage.py runserver
```

Run tests to check the App is ok:
```sh
python manage.py test
```

## Application

After setup, the application should be up and running, so go to your web-browser and open the http://127.0.0.1:8000/admin/ url, there you will see the admin site.
In the admin site, selecting a currency will show a chart of the exchange rates for that currency as base, you can see it for instance at http://127.0.0.1:8000/admin/exchange_rate/currency/1/change/ url


## API

The endpoints to use the API are the following:
 - Currency rates: http://127.0.0.1:8000/api/currency_rates?source_currency=EUR&date_from=2021-02-08&date_to=2021-02-14
 - Exchanged currency amount: http://127.0.0.1:8000/api/exchanged_currency_amount?source_currency=EUR&exchanged_currency=GBP&amount=1.3
 - Time weighted rate: http://127.0.0.1:8000/api/twr?source_currency=EUR&exchanged_currency=GBP&amount=1.3&date_from=2020-05-15



## Considerations

These are some considerations, decissions and asumptions I took when designing and developing the project: 
- I found a package to retrieve the data from Fixer.io provider, so I installed and used it.
- I developed a small client to generate random data.
- I've split the project in several applications:
  - exchange_rate: This is the core app, here is where the main application logic is handled.
  - api: This app manage the API requests
  - random_exchange: This is the client that provides random data for currency exchange rates
- Since each provider has a different interface to retrieve the rates info, I've created two adapters, one for each provider. This allows the main app, through the adaptor, to make requests to each provider using allways the same interface, so the app knows how to talk to the adaptor, and every adaptor knows how to talk to its provider. 
- In the provider model is also stored the class of the adaptor it uses. That way is very easy to get the adaptor for each provider. 
- Everytime a new rate is needed, the app will try and fetch it from the database, in case that the data is not available there, it will try and find it in the providers configured, following the priority order, where 1 is higher priority than two and so on.
- After calling a provider to retrieve a rate, the returned data is stored in the database.
- Currently when the app needs to retrieve rates from a provider for a range of days, this requests are made synchronously in a loop. This can be improved by using async task with celery, so many requests can be done at the same time, using the celery approach it will be neede to pay more attention in the managing of the data to avoid duplicated values in the database.
- Currently I'm storing data into the database using bulk functions.
- I've used the amCharts library to show the charts because I've used before and is very easy to integrate.
- I have assumed that is not necessary to know the provider of the data stored in the database, in case that needed, a new field shold be added to the model to store this provider, and take into the account its priority. 


## Links

1. Django: https://www.djangoproject.com/
2. amCharts: https://www.amcharts.com/
3. Fixer: https://fixer.io/
4. Adapters in Django: https://charlesleifer.com/blog/django-patterns-pluggable-backends/


