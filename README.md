# Overview
This is a simple dashboarding web application built using Flask, Bootstrap, and D3.  The application has been tested with Python 2.7.

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

4. Run tests
```
./manage.py test
```

5. Start development server
```
./manage.py runserver
```

# Database Operations
**Destroy and Rebuild Database**
```
./manage db_rebuild
```

**Migrations**
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
* [SB Admin Bootstrap Template](http://startbootstrap.com/template-overviews/sb-admin/)
* [D3 Documentation](http://d3js.org/)
* [Miguel Grinberg Flask Web Development Book](http://www.flaskbook.com/)
* [Miguel Grinberg Flask Web Development GitHub](https://github.com/miguelgrinberg/flasky)
