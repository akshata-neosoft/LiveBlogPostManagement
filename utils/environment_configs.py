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

    """Redis"""
    layer = configs['REDIS']['layer']
    layer_password = configs['REDIS']['layer_password']
    layer_host = configs['REDIS']['layer_host']
    layer_port = configs['REDIS']['layer_port']

    """ Email"""
    email_backend = configs['EMAIL']['EMAIL_BACKEND']
    email_host = configs['EMAIL']['EMAIL_HOST']
    email_port = int(configs['EMAIL']['EMAIL_PORT'])
    email_use_tls = configs['EMAIL'].getboolean('EMAIL_USE_TLS')
    email_host_user = configs['EMAIL']['EMAIL_HOST_USER']
    email_host_password = configs['EMAIL']['EMAIL_HOST_PASSWORD']
    default_from_email = configs['EMAIL']['DEFAULT_FROM_EMAIL']

    """Celery"""
    celery_broker_url = 'redis://localhost:6379/0'
    celery_result_backend = 'redis://localhost:6379/0'
    celery_accept_token = ['json']
    celery_task_serializer = 'json'




