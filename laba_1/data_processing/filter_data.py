from .get_data import URL

import requests

def filterType(engName):
    if engName == 'ALL':
        return requests.get(URL + 'products/?status=A').json()
    return requests.get(URL + f'products/?type={engName}&status=A').json()