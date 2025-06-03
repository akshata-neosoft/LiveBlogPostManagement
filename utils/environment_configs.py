import configparser

configs = configparser.ConfigParser()
configs.read('config.ini')
configs.sections()


class EnvironmentConfigs:
    """
    Central DB
    """
    db = configs['DATABASE']['db']
    dbName = configs['DATABASE']['dbName']
    dbHost = configs['DATABASE']['dbHost']
    dbPort = configs['DATABASE']['dbPort']
    dbUser = configs['DATABASE']['dbUser']
    dbPassword = configs['DATABASE']['dbPassword']

    """Communication salt"""
    internal_salt = configs['INTERNAL']['INTERNAL_SALT']
    internal_pass = configs['INTERNAL']['INTERNAL_PASS']

    """Redis"""
    layer = configs['REDIS']['layer']
    layer_password = configs['REDIS']['layer_password']
    layer_host = configs['REDIS']['layer_host']
    layer_port = configs['REDIS']['layer_port']

