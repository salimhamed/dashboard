# Overview
This is a simple dashboarding web application built using Flask, Bootstrap, and D3.  The application has been tested with Python 2.7.

# Installation
**Clone the repository**
```
git clone https://github.com/salimhamed/dashboard.git
```

**Create a virtualenv in the project directory**
```
cd dashboard
virtualenv venv
source venv/bin/activate
```

**Install dependencies**
```
pip install -r requirements.txt
```

**Run tests**
```
./manage.py test
```

**Start development server**
```
./manage.py runserver
```

# Database Operations
**Migrations**
```
# create automatic migration script (review upgrade script before applying)
./manage db migrate -m "<migration message>"

# apply migration upgrade script
./manage db upgrade
```

# Resources
* [Flask Documentation](http://flask.pocoo.org/)
* [Bootstrap Documentation](http://getbootstrap.com/)
* [D3 Documentation](http://d3js.org/)
* [Miguel Grinberg Flask Web Development Book](http://www.flaskbook.com/)
* [Miguel Grinberg Flask Web Development GitHub](https://github.com/miguelgrinberg/flasky)
