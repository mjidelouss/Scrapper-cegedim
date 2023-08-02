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


    try:

        result = data.find('div', {'id': 'result_deno_societe'})

        if result:
            link = result.find('a')['href']
            return link
        else:
            print("Link not found.")
            # return res

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except Exception as e:
            print(f"An unexpected error occurred: {e}")

def ScrapingData(data):


    res = {
        "WebSite": "societe",
        "RaisonSociale": "",
        "Adresse": "",
        "SIREN": "",
        "Tva": "",
    }

    try:

        table = data.find("table")
        tr = table.find_all("tr")

        for td in tr:
            if td.find("td", class_="break-word") != None:
                res["RaisonSociale"] = td.find("td", class_="break-word").text
            if td.find('a', class_="Lien secondaire") != None:
                Adresse = td.find('a', class_="Lien secondaire").text
                Adresse = Adresse.replace('\n', '')
                Adresse = Adresse.replace('                    ', '')
                res["Adresse"] = Adresse
            if td.find('div', id="tva_number") != None:
                div = td.find('div', id="tva_number")
                res["Tva"] = div.find("span").text
            if td.find("div", id="siren_number") != None:
                div = td.find("div", id="siren_number")
                res['SIREN'] = div.find('span').text

        return res

    except:

        return res















