from django.http import HttpResponse
from django.template import loader
from .backEnd import societe
from .backEnd import verif
from .backEnd import infogreffe
from .backEnd import lefigaro
def index(request):

    siren = ""
    ArrayOb = []

    if request.method == "POST":
        data = request.POST
        siren = data.get('siren')
        WebSite = data.getlist('WebSite')

        # if data.is_valid():
        #     siren = data.get('siren')

        for ws in WebSite:
            if ws == "Verify":
                # verif
                link = "https://www.verif.com/recherche/" + siren
                responseCon = verif.connection(link)
                data = verif.getContent(responseCon)
                resultVerif = verif.tritement(data)
                ArrayOb.append(resultVerif)
            if ws == "Societe":
                # societe getLink scraping 1
                link = "https://www.societe.com/cgi-bin/search?champs=" + siren
                responseCon = societe.connection(link)
                data = societe.getContent(responseCon)
                getLink = societe.tritement(data)

                try:
                    # societe scraping 2
                    responseCon = societe.connection("https://www.societe.com/" + getLink)
                    dataFin = societe.getContent(responseCon)
                    resultSociete = societe.ScrapingData(dataFin)
                    ArrayOb.append(resultSociete)
                except:
                    print("Data Not Found")

                    res = {
                        "WebSite": "societe",
                        "RaisonSociale": "Not Found",
                        "Adresse": "Not Found",
                        "SIREN": "Not Found",
                        "Tva": "Not Found",
                    }

                    ArrayOb.append(res)

            if ws == "lefigaro":
                # lefigaro
                link = "https://entreprises.lefigaro.fr/recherche?q=" + siren
                responseCon = lefigaro.connection(link)
                data = lefigaro.getContent(responseCon)
                resulefigarof = lefigaro.tritement(data)
                ArrayOb.append(resulefigarof)
            if ws == "infogreffe":
                # infogreffe
                link = 'https://www.api.infogreffe.fr/athena/recherche-api/recherche/entreprises_etablissements?phrase=' + siren
                responseCon = infogreffe.connection(link)
                data = infogreffe.getContent(responseCon)
                resultInfogreffe = infogreffe.tritement(data)
                ArrayOb.append(resultInfogreffe)
            if ws == "":
                ArrayOb.clear()
    else:
        ArrayOb.clear()

    context = {
        'ArrayOb': ArrayOb,
    }

    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))