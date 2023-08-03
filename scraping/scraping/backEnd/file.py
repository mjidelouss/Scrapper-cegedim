import pandas as pt
import difflib

def Search(data):
    try:

        SIREN = data.get("SIREN DEDUIT")
        SIREN = SIREN.values.tolist()
        listSiren = []
        for s in SIREN:
            string = str(s)
            if len(string) == 8:
                res = "0"+string
                listSiren.append(res)
            elif len(string) == 7:
                res = "00"+string
                listSiren.append(res)
            elif len(string) == 6:
                res = "000"+string
                listSiren.append(res)
            else:
                listSiren.append(string)
        return listSiren

    except FileNotFoundError:
        print(f"File not found")
    except Exception as e:
        print(f"An error occurred: {e}")
def address_match(address1, address2, address3, address4):
    address1_normalized = address1.lower().strip()
    address2_normalized = address2.lower().strip()
    address3_normalized = address3.lower().strip()
    address4_normalized = address4.lower().strip()

    similarity_ratio_1_2 = difflib.SequenceMatcher(None, address1_normalized, address2_normalized).ratio()
    similarity_ratio_1_3 = difflib.SequenceMatcher(None, address1_normalized, address3_normalized).ratio()
    similarity_ratio_1_4 = difflib.SequenceMatcher(None, address1_normalized, address4_normalized).ratio()

    return similarity_ratio_1_2 >= 0.7 and similarity_ratio_1_3 >= 0.7 and similarity_ratio_1_4 >= 0.7

def DIFFERENCE(resultVerif,resulefigarof,resultInfogreffe,resultSociete):
    for field in ["RaisonSociale", "Adresse", "SIREN", "Tva"]:
        if field != "Adresse" and field != "Tva":
            if resultVerif[field] != resultSociete[field] or resulefigarof[field] != resultInfogreffe[field] or resultSociete[field] != resulefigarof[field]:
                resultSociete['DIFFERENCE'] = resultSociete['DIFFERENCE'] + "- " + field
                resultInfogreffe['DIFFERENCE'] = resultInfogreffe['DIFFERENCE'] + "- " + field
                resulefigarof['DIFFERENCE'] = resulefigarof['DIFFERENCE'] + "- " + field
                resultVerif['DIFFERENCE'] = resultVerif['DIFFERENCE'] + "- " + field
        if field == "Adresse" and not address_match(resultSociete['Adresse'], resultInfogreffe['Adresse'], resulefigarof['Adresse'], resultVerif['Adresse']):
            resultSociete['DIFFERENCE'] = resultSociete['DIFFERENCE'] + "- " + field
            resultInfogreffe['DIFFERENCE'] = resultInfogreffe['DIFFERENCE'] + "- " + field
            resulefigarof['DIFFERENCE'] = resulefigarof['DIFFERENCE'] + "- " + field
            resultVerif['DIFFERENCE'] = resultVerif['DIFFERENCE'] + "- " + field

        # Print the comparison details
    if resultVerif["Tva"] != resultSociete["Tva"] != resulefigarof["Tva"]:
        resultSociete['DIFFERENCE'] = resultSociete['DIFFERENCE'] + "- Tva"
        resultInfogreffe['DIFFERENCE'] = resultInfogreffe['DIFFERENCE'] + "- Tva"
        resulefigarof['DIFFERENCE'] = resulefigarof['DIFFERENCE'] + "- Tva"
        resultVerif['DIFFERENCE'] = resultVerif['DIFFERENCE'] + "- Tva"
