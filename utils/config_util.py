import json
import requests


def get_env(env):
    if env in ['DEV', 'UAT', 'LOCALHOST']:
        env_data = _read_config('config.json', env)
        authorization_header = _get_authorization(env)
    else:
        raise TypeError('Unexpected Env. DEV, UAT and LOCALHOST are available')
    return {'data': env_data,
            'headers': authorization_header}


def _read_config(file, tag):
    with open(file) as json_file:
        as_dict = json.load(json_file)[tag]
        return as_dict


def _get_authorization(env):
    headers = {}
    env_data = _read_config('config.json', env)
    if env == 'DEV' or env == 'UAT':
        response = requests.post(url=''.join([env_data['auth0']['domain_auth0'], '/oauth/token']),
                                 data=env_data['auth0']['payload_auth0'])
        headers = {'Authorization': 'Bearer {}'.format(response.json()['id_token'])}
    return headers
