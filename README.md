# Overview

This is a simple dashboarding application built using Flask and Bootstrap.  The application has been tested with Python 2.7. It's ready to deploy with [AWS Elastic Beanstalk](http://aws.amazon.com/elasticbeanstalk/).

# Installation

1. Clone the repository

  ```
  git clone https://github.com/salimhamed/dashboard.git
  ```

2. Create a virtualenv in the project directory

  ```
  cd dashboard
  virtualenv venv
  source venv/bin/activate
  ```

3. Install dependencies

  ```
  pip install -r requirements.txt
  ```

4. Create database

  ```
  ./manage db_rebuild
  ```

5. Run tests

  ```
  ./manage.py test
  ```

6. Start development server

  ```
  ./manage.py runserver
  ```

# Database Operations

**PostgreSQL Database Operations**

1. `pg_ctl` is a utility to initialize, start, stop, or control a PostgreSQL server.
  * `pg_ctl status -D DATADIR` shows the status of a PostgreSQL database.
  * `pg_ctl start -D DATADIR` starts the PostgreSQL server
  * `pg_ctl stop -D DATADIR` stops the PostgreSQL server.
  * `pg_ctl stop -D DATADIR -m fast` immediately stops the PostgreSQL server rather than waiting for session-initiated disconnection.
2. `postgres` is the PostgreSQL server.
  * `postgres -D DATADIR` starts the PostgreSQL server.
3. `psql` is the PostgreSQL interactive terminal.
  * `psql -d DATABASE` connects to a given database.
  * `psql -l` lists all available databases.

**Destroy and Rebuild Database**

1. The positional argument 'db_rebuild' will delete any existing sqlite database and create a new devlopment database populated with fake data.

  ```
  ./manage db_rebuild
  ```

**Database Migrations**

1. Create an automatic migration upgrade script

  ```
  ./manage db migrate -m "<migration message>"
  ```

2. Apply the migration upgrade script (note, upgrade script should be reviewed before applying changes)

  ```
  ./manage db upgrade
  ```

# Resources

* [Flask Documentation](http://flask.pocoo.org/)
* [Bootstrap Documentation](http://getbootstrap.com/)
* [SB Admin 2 Bootstrap Template](http://startbootstrap.com/template-overviews/sb-admin-2/)
* [Miguel Grinberg Flask Web Development Book](http://www.flaskbook.com/)
* [Miguel Grinberg Flask Web Development GitHub](https://github.com/miguelgrinberg/flasky)

# Flask Extensions
* [Flask Bootstrap](http://pythonhosted.org/Flask-Bootstrap/)
* [Flask Mail](https://pythonhosted.org/Flask-Mail/)
* [Flask Moment](https://github.com/miguelgrinberg/flask-moment/)
* [Flask SQLAlchemy](https://pythonhosted.org/Flask-SQLAlchemy/)
* [Flask Migrate](https://flask-migrate.readthedocs.org/en/latest/)
* [Flask Login](https://flask-login.readthedocs.org/en/latest/)
* [Flask Script](http://flask-script.readthedocs.org/en/latest/)
