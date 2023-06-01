"""
Geography API (https://rapidapi.com/mmplabsadm/api/geography4)
Get summarized or detailed view of Countries.
{
        "href": "/apis/geography/v1/country/CAN",
        "name": {
            "common": "Canada",
            "official": "Canada"
        },
        "flags": {
            "png": "https://flagcdn.com/w320/ca.png",
            "svg": "https://flagcdn.com/ca.svg"
        }
    },

"""
import requests

from utils import colors

API_KEY = "YOUR_API_KEY"
API_HOST = "geography4.p.rapidapi.com"

URL = "https://geography4.p.rapidapi.com/apis/geography/v1/country"

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}


def get_countries() -> dict:
    """
    Get a list of countries objects from API.
    :return: countries information (dict)
    """
    try:
        return requests.get(URL, headers=HEADERS, timeout=5).json()
    except (requests.exceptions.Timeout,
            requests.exceptions.HTTPError,
            requests.exceptions.ConnectionError,
            requests.exceptions.RequestException):
        return f"{colors.get('red')}Request error. \n" \
               'Check your internet connection and make sure the website is accessible.' + \
            colors.get('default')


countries = get_countries()


def get_country_flags(countries_name: str) -> list:
    """
    Get country's flags based on countries name.
    :param countries_name: str
    :return: urls of country flags (list)
    """
    urls = []
    for country_name in countries_name.split(', '):
        urls.append("".join([country['flags']['png']
                             for country in countries
                             if country['name']['common'] == country_name]))
    return urls
