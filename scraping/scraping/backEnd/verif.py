from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPProxyAuth
def connection(path):

    s = requests.Session()

    proxies = {
      "http": "http://isp-ceg.emea.cegedim.grp:3131",
      "https": "http://isp-ceg.emea.cegedim.grp:3131"
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    auth = HTTPProxyAuth("rdaoudi", "Cegedim1")

    s.proxies = proxies
    s.auth = auth
    response = s.get(path , headers=headers)
    return response

def getContent(connection):

    soup = BeautifulSoup(connection.content, 'html.parser')
    return soup


def tritement(data):

    table = data.find_all("tr", class_="bg")

    res = {
        "WebSite": "Verif",
        "RaisonSociale": "Not Found",
        "Adresse": "Not Found",
        "SIREN": "Not Found",
        "Tva": "Not Found",
        "DIFFERENCE": ""
    }

    try:
        strong = data.find('strong', id="dirigeant")
        span = strong.find('span').text
        span = span.replace('- ', '')
        span = span.replace('                    ', '')
        res["RaisonSociale"] = span

        siren = data.find("tr", class_="siren bg")
        siren = siren.find_all("td")[1].text
        siren = siren.replace(" ", "")
        res["SIREN"] = siren
    except:

        print("Data Not Found for verif")
        return res

    for td in table:
        if td.find('td', class_="numero-tva") != None:
            res["Tva"] = td.find('td', class_="numero-tva").text
        if td.find('div', class_="pull-left") != None:
            div = td.find('div', class_="pull-left")
            streetAddress = div.find('span', itemprop="streetAddress").text
            postalCode = div.find('span', itemprop="postalCode").text
            addressLocality = div.find('span', itemprop="addressLocality").text
            res["Adresse"] = streetAddress + " " + postalCode + " " + addressLocality

    return res






