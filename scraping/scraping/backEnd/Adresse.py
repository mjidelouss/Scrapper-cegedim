from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPProxyAuth
import re

def get_soup(link, proxy_url, auth):
    with requests.Session() as session:
        session.proxies = {'http': proxy_url, 'https': proxy_url}
        session.auth = auth
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }
        response = session.get(link, headers=headers, timeout=5)
        response.raise_for_status()  # raise an exception if the request fails
        return BeautifulSoup(response.text, 'html.parser')

def googleSearch(query, num_results=10):
    try:
        url = "https://www.google.com/search?q=siren " + query

        auth = HTTPProxyAuth("rdaoudi", "Cegedim1")

        proxies = "http://isp-ceg.emea.cegedim.grp:3131"

        soup = get_soup(url, proxies, auth)

        search_result_links = []
        for link_element in soup.select('div.yuRUbf a'):
            search_result_links.append(link_element['href'])

        return search_result_links[:num_results]

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the search: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def search(input):
    links = googleSearch(input, num_results=10)

    numbers = []
    for link in links:
        extracted_numbers = re.findall(r'\d{9,}', link)
        for num_str in extracted_numbers:
            numbers.append(int(num_str[0:9]))

    unique_numbers = set()
    duplicate_numbers = []
    for num in numbers:
        if num in unique_numbers:
            duplicate_numbers.append(num)
        else:
            unique_numbers.add(num)
        unique_duplicates = list(set(duplicate_numbers))

    return unique_duplicates




