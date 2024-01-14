# Budget Management

Application allows adding expenses and generating pdf report based on them.

## How to run locally
- To run that application properly, installed Docker is required
- At terminal go to `home_budget` directory and run `docker-compose up -d`

## API

1. Open Swagger view with all possible endpoints and theirs descriptions:
`http://localhost:8000/`

or

2. Open API Root view based on django-rest-framework:
`http://localhost:8000/api/`

3. To work with this app, user needs to be logged in. There is a default user called 
`TestUser`, which has some test data already added to play with - you can generate
new pdf report based on them (years 2019-2023) or add new expenses.
To login click `Django Login` button at swagger view or `Log in` button at DRF view
and use the following credentials:
login - `TestUset`, password - `testpassword1`

4. To run tests and check coverage, enter to the running app container with 
`docker exec -it <container_id> /bin/sh` and run the following command 
`coverage run -m pytest && coverage report && coverage html`