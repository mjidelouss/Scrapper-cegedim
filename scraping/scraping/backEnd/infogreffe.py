from bs4 import BeautifulSoup
import requests
from requests.auth import HTTPProxyAuth
import json

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
    response = s.get(path)
    return response

def getContent(connection):

    soup = BeautifulSoup(connection.content, 'html.parser')
    return soup

def tritement(data):

    res = {
        "WebSite": "infogreffe",
        "RaisonSociale": "Not Found",
        "Adresse": "Not Found",
        "SIREN": "Not Found",
        "Tva": "Not Found",
        "DIFFERENCE": ""
    }

    try:
        content = data.text
        content = json.loads(content)

        ligne1 = content["data"][0]["adresse"]['adresse_declaree']['ligne1']
        ligne2 = content["data"][0]["adresse"]['adresse_declaree']['ligne2']
        ligne3 = content["data"][0]["adresse"]['adresse_declaree']['ligne3']
        adresse = ""

        if ligne1 != None:
            adresse += ligne1
        if ligne2 != None:
            adresse += ligne2
        if ligne3 != None:
            adresse += ligne3

        codePostal = content["data"][0]["adresse"]['adresse_declaree']['code_postal']
        ville = content["data"][0]["adresse"]['adresse_declaree']['bureau_distributeur']
        RaisonS = content["data"][0]["nom_entreprise"]
        res["RaisonSociale"] = RaisonS.upper()
        res["Adresse"] = adresse+" "+codePostal+" "+ville
        res["SIREN"] = content["data"][0]["numero_identification"]
        res["Tva"] = "not found"

        return res

    except:
        return res

