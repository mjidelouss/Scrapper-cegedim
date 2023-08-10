from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from .backEnd import societe
from .backEnd import verif
from .backEnd import infogreffe
from .backEnd import lefigaro
from .backEnd import file
from .backEnd import createExel
from .backEnd import Adresse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from django.contrib import messages


def index(request):
    ArrayOb = []
    if request.method == "POST":
        data = request.POST
        siren = data.get('siren')
        WebSite = data.getlist('WebSite')
        if len(siren) <= 11:
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

            ArraySiren = Adresse.search(siren)
            context = {
                'ArraySiren': ArraySiren,
            }


            template = loader.get_template('home.html')
            return HttpResponse(template.render(context, request))

    else:
        ArrayOb.clear()

    context = {
        'ArrayOb': ArrayOb,
    }

    template = loader.get_template('home.html')
    return HttpResponse(template.render(context, request))




@csrf_exempt
def import_(request):
    if request.method == "POST":
        excel_file = request.FILES["excel_file"]
        data = pd.read_excel(excel_file)
        ListSiREN = file.Search(data)
        data = Tritement(ListSiREN)
        # export(data)
        createExel.export_users_xls(data)
        # context = {
        #     'exportData': exportData,
        # }
    messages.success(request, 'Successfully completed the task!')

    return redirect('index')


def Tritement(request):
    ArrayOb = []
    for siren in request:
        # verif
        link = "https://www.verif.com/recherche/" + siren
        responseCon = verif.connection(link)
        data = verif.getContent(responseCon)
        resultVerif = verif.tritement(data)
        ArrayOb.append(resultVerif)
        # societe getLink scraping 1
        link = "https://www.societe.com/cgi-bin/search?champs=" + siren
        responseCon = societe.connection(link)
        data = societe.getContent(responseCon)
        getLink = societe.tritement(data)

        # lefigaro
        link = "https://entreprises.lefigaro.fr/recherche?q=" + siren
        responseCon = lefigaro.connection(link)
        data = lefigaro.getContent(responseCon)
        resulefigarof = lefigaro.tritement(data)
        ArrayOb.append(resulefigarof)

        # infogreffe
        link = 'https://www.api.infogreffe.fr/athena/recherche-api/recherche/entreprises_etablissements?phrase=' + siren
        responseCon = infogreffe.connection(link)
        data = infogreffe.getContent(responseCon)
        resultInfogreffe = infogreffe.tritement(data)
        ArrayOb.append(resultInfogreffe)
        if getLink:
            # societe scraping 2
            responseCon = societe.connection("https://www.societe.com/" + getLink)
            dataFin = societe.getContent(responseCon)
            resultSociete = societe.ScrapingData(dataFin)
            ArrayOb.append(resultSociete)
            file.DIFFERENCE(resultVerif, resulefigarof, resultInfogreffe, resultSociete)
        else:
            print("Data Not Found")

            res = {
                "WebSite": "societe",
                "RaisonSociale": "Not Found",
                "Adresse": "Not Found",
                "SIREN": "Not Found",
                "Tva": "Not Found",
                "DIFFERENCE": ""
            }

            ArrayOb.append(res)

    return ArrayOb


def Export(request):
    file_name = "download.xlsx"
    sheet_name = "Sheet1"
    createExel.create_excel_file(file_name, sheet_name, request)
