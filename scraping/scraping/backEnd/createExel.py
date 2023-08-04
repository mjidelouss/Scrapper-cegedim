import xlwt
from django.http import HttpResponse
from datetime import datetime

def create_excel_file(file_name, sheet_name, data):
    print("fdf")
    # export_users_xls(data)
    # workbook = openpyxl.Workbook()
    # sheet = workbook.active
    # sheet.title = sheet_name
    #
    # header_row = ["WebSite", "Raison sociale", "Adresse", "Siren" , "Tva" ,"DIFFERENCE"]
    # for col_index, cell_value in enumerate(header_row, start=1):
    #     sheet.cell(row=1, column=col_index, value=cell_value)
    # for row_index, row_data in enumerate(data, start=2):
    #     row_data = row_data.values()
    #     my_list = list(row_data)
    #     for col_index, cell_value in enumerate(my_list, start=1):
    #         sheet.cell(row=row_index, column=col_index, value=cell_value)
    #
    # # workbook.save(file_name)
    #
    # file_path = file_name
    #
    # with open(file_path, 'rb') as excel_file:
    #     # Prepare the response object with appropriate headers
    #     response = HttpResponse(excel_file.read(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #
    #     # Set the file name for the user to download
    #     response['Content-Disposition'] = 'attachment; filename=azazaza.xlsx'
    #
    # print(f"File '{file_name}' with sheet '{sheet_name}' has been created.")

import pandas as pd
import os
def export_users_xls(data):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    df = pd.DataFrame(data)
    home_dir = os.path.expanduser("~")

    path = home_dir + '\Downloads'




    df.to_excel(path + 'Download.xlsx', index=False)

    df.to_excel(os.path.join(path, 'Download.xlsx'))

    # data = [{'WebSite': 'verif', 'RaisonSociale': 'GRANDS MOULINS AUTO', 'Adresse': 'LES GRANDS MOULINS 88200 ST ETIENNE LES REMIREMONT', 'SIREN': '379043938','Tva': 'FR50379043938','DIFFERENCE': ''}, {'WebSite': 'lefigaro', 'RaisonSociale': 'GRANDS MOULINS AUTO', 'Adresse': 'LES GRANDS MOULINS 88200 SAINT-ETIENNE-LES-REMIREMONT', 'SIREN': '379043938', 'Tva': 'FR50379043938', 'DIFFERENCE': ''}, {'WebSite': 'infogreffe', 'RaisonSociale': 'GRANDS MOULINS AUTO', 'Adresse': 'Parc Economique des Grands Moulins 88200 Saint-Étienne-lès-Remiremont', 'SIREN': '379043938', 'Tva': 'not found', 'DIFFERENCE': ''}, {'WebSite': 'societe', 'RaisonSociale': 'GRANDS MOULINS AUTO', 'Adresse': 'LES GRANDS MOULINS 88200 SAINT-ETIENNE-LES-REMIREMONT', 'SIREN': '379043938', 'Tva': 'FR50379043938', 'DIFFERENCE': ''}, {'WebSite': 'verif', 'RaisonSociale': 'INTERCONTROLE', 'Adresse': '54 RUE D ARCUEIL 94150 RUNGIS', 'SIREN': '305254526', 'Tva': 'FR73305254526', 'DIFFERENCE': ''}, {'WebSite': 'lefigaro', 'RaisonSociale': 'INTERCONTROLE', 'Adresse': '54 Rue D ARCUEIL 94150 RUNGIS', 'SIREN': '305254526', 'Tva': 'FR73305254526', 'DIFFERENCE': ''}]

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Download_'+dt_string+'.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ["WebSite", "Raison sociale", "Adresse ", "Siren", "Tva", "DIFFERENCE"]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    data_array_list = [list(d.values()) for d in data]
    for row in data_array_list:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response

    # template = loader.get_template('home.html')
    # return HttpResponse(template.render(response))
