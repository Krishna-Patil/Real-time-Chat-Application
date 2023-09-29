# Real-time-Chat-Application

### Clone the repository
`git clone https://github.com/Krishna-Patil/Real-time-Chat-Application.git`

### Change into Real-time-Chat-Application directory
`cd Real-time-Chat-Application`

### Activate virtual environment and install dependecies
Note: install pipenv if you don't have already, using pip  
`pipenv shell`  
`pipenv sync`  

### Install redis if you don't have already
for mac  
`brew install redis`  
then run  
`redis-server`  

### Migrate all changes
`python manage.py migrate`  

### Runserver
`python manage.py runserver`
