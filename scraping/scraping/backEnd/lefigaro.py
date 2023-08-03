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
    response = s.get(path , headers=headers)
    return response

def getContent(connection):

    soup = BeautifulSoup(connection.content, 'html.parser')
    return soup


def tritement(data):

    res = {
        "WebSite": "lefigaro",
        "RaisonSociale": "Not Found",
        "Adresse": "Not Found",
        "SIREN": "Not Found",
        "Tva": "Not Found",
        "DIFFERENCE": ""
    }

    try:
        content = data.find_all("script", type="application/ld+json")[1]
        content = content.text
        content = json.loads(content)

        RaisonSociale = content['legalName']
        Serin = content['identifier']['value']
        Tva = content['vatID']
        streetAddress = content['address']['streetAddress']
        postalCode = content['address']['postalCode']
        addressLocality = content['address']['addressLocality']
        Adresse = streetAddress +" "+postalCode +" "+addressLocality

        res["RaisonSociale"] = RaisonSociale
        res["Adresse"] = Adresse
        res["SIREN"] = Serin
        res["Tva"] = Tva
        return res

    except:
        return res

    # content = data.find('main', class_='layout_main')
    # main = content.find_all("div", class_="grid_left w60 ccmcss_align_l ccmcss_valign_c")
    # dd = content
    # if len(main) == 0:
    #
    #     try:
    #         dd = dd.find_all("dd")
    #         RaisonSociale = dd[0].text
    #
    #         Serin = dd[2].text
    #         Serin = Serin[0:9]
    #
    #         Tva = dd[4].text
    #         Tva = Tva.replace(" ", "")
    #         Tva = Tva.replace("(ensavoirplus)", "")
    #
    #         # convert str to object
    #         TvaScript = data.find_all("script", type="application/ld+json")[1]
    #         TvaScript = TvaScript.text
    #         TvaScript = json.loads(TvaScript)
    #
    #         if TvaScript['vatID'] != Tva or TvaScript['vatID'] == Tva :
    #             res["Tva"] = TvaScript['vatID']
    #
    #
    #         Adresse = data.find("address").find_all('br')
    #         Adresse = " ".join(line.next_sibling.strip() for line in Adresse)
    #
    #         res["Raison sociale"] = RaisonSociale
    #         res["Adresse"] = Adresse
    #         res["SIREN"] = Serin
    #
    #
    #         return res
    #     except:
    #         return "Data Not Found for letigaro"
    #
    # elif len(main) != 0:
    #
    #     try:
    #         RaisonSociale = main[0].text
    #         RaisonSociale = RaisonSociale.replace("\n", "")
    #         RaisonSociale = RaisonSociale.replace("\r", "")
    #         RaisonSociale = RaisonSociale.strip()
    #
    #         Serin = main[1]
    #         Serin = Serin.find('span').text
    #
    #         Tva = main[3].text
    #         Tva = Tva.replace(" ", "")
    #         Tva = Tva.replace("\n", "")
    #         Tva = Tva.replace("\r", "")
    #         Tva = Tva.replace("(ensavoirplus)", "")
    #
    #         Adresse = data.find("address").find_all('br')
    #         Adresse = " ".join(line.next_sibling.strip() for line in Adresse)
    #
    #         res["Raison sociale"] = RaisonSociale
    #         res["Adresse"] = Adresse
    #         res["SIREN"] = Serin
    #         res["Tva"] = Tva
    #         return res
    #     except:
    #         return "Data Not Found for letigaro"


# if __name__ == "__main__":
#     siren = "314397670"
#     siren = "348582834"
#     siren = "775662257"
#     link = "https://entreprises.lefigaro.fr/recherche?q=" + siren
#     responseCon = connection(link)
#     data = getContent(responseCon)
#     resultVerif = tritement(data)
#     print(resultVerif)