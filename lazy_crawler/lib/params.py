import os


def get_params():
    """
    returns a dict of parameters  passed from the app.live.grepsr.com
    :return:
    """
    try:
        return eval(os.environ.get('RUN_PARAMETERS', {}))
    except:
        return {}
