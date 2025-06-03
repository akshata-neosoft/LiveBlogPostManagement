import logging

service_logger = logging.getLogger('service_logger')

action_logger = logging.getLogger('action_logger')


def log_action_msg(username, role, message, log_type):
    """
    This function will get the inputs from service and will merge them into action logger format
    :param username: actor
    :param role: roles of the actor
    :param message: action performed
    :param log_type: level of the log
    """
    try:
        action_logger.info(message, extra={"Username": username, "Role": ','.join(role),
                                           "LogType": "Action", "level": log_type})

    except Exception as e:
        action_logger.error(e)
