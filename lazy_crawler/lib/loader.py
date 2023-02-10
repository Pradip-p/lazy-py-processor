import pandas as pd
import os
from typing import Union


def _loader(filename, file_type):
    if file_type == 'csv':
        return pd.read_csv(filename)
    elif file_type == 'json':
        return pd.read_json(filename)
    elif file_type == 'excel':
        return pd.read_excel(filename)
    else:
        raise Exception(f'File type: {file_type} not supported')


def load_file(file: str, project: str, file_type='csv', is_url: bool = False, ):
    """
    It will try to read the file from disk by default. use `is_url` flag to load via url.
    In case of url. It will first download the  file via request library and then load it.
    if a valid content type cannot be detected

    :param file:  filename to load or the url
    :param project: Name of project
    :param file_type: str (example:csv,json,xlsx) default = csv
    :param is_url: pass True if the file is url
    :return: pandas dataframe
    """
    if not is_url:
        if os.environ.get('APP_ENV', 'dev').upper() == 'DEV':
            file = os.getcwd() + '/' + project + '/' + file
        else:
            file = '' + project + '/' + file

    df = _loader(file, file_type)
    return df
