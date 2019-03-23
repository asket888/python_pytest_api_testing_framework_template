# python-api-testing-framework-template:
This is a template of API testing framework in Python. Following stack is using:

pytest
requests
prospector
allure

# Setup
1. git clone `git@github.com:asket888/python-api-testing-framework-template.git`
2. `cp config.json.example config.json`
3. Add actual passwords for all tested environments

# Command line Execution:
1. navigate to project directory
2. run `pipenv install` to setup all necessary dependencies from Pipfile.lock
3. run `pipenv shell` to be able use all pipenv dependencies from terminal
4. to run tests use command `$ invoke run` (DEV env is set up by default)
5. to run tests with allure-report creating use command `$ invoke run-with-allure` (DEV env is set up by default)

# Tests parametrization:
1. to run tests on specific env (e.g: LOCALHOST) use command `$ invoke run --env=LOCALHOST`
2. to run tests with specific mark (e.g: @pytest.mark.health) use command `$ invoke run --tags=health`
