from invoke import task


@task
def run(context, env='', tags=''):
    """
    Run tests without allure report generating
    :param context: invoke context object
    :param env: run tests on specific environment (DEV, UAT, LOCALHOST)
    :param tags: run only tests marked by specific tag
    :keyword: '$ invoke run'
    :keyword: '$ invoke run --tags=@health'
    """
    pytest_cmd = 'python -m pytest ./api --show-capture=stdout'
    if env != '':
        pytest_cmd = ' --env='.join([pytest_cmd, env])
    if tags != '':
        pytest_cmd = ' -m '.join([pytest_cmd, tags])
    context.run(pytest_cmd)


@task
def run_with_allure(context, env='', tags=''):
    """
    Run tests with html allure report generating
    :param context: invoke context object
    :param env: run tests on specific environment (DEV, UAT, LOCALHOST)
    :param tags: run only tests marked by specific tag
    :keyword: '$ invoke run-with-allure'
    :keyword: '$ invoke run-with-allure --tags=@main_menu'
    """
    pytest_cmd = 'python -m pytest ./api --alluredir artifacts --show-capture=stdout'
    if env != '':
        pytest_cmd = ' --env='.join([pytest_cmd, env])
    if tags != '':
        pytest_cmd = ' -m '.join([pytest_cmd, tags])
    context.run(pytest_cmd)
