# server/utils.py

import requests

class CompanyInfo:
    def __init__(self, nrRegCom, cui, denumire, sdenumire_Strada, snumar_Strada, sdenumire_Judet, scod_JudetAuto, sdenumire_Localitate, scpTVA, sdetalii_Adresa):
        self.company_registration_number = nrRegCom
        self.company_tin = cui
        self.company_name = denumire
        self.company_address_country_subentity = sdenumire_Judet
        self.company_address_country = 'Romania'
        self.company_address_country_code = 'RO'
        self.company_address_country_subentity_code = scod_JudetAuto
        self.company_address_city = sdenumire_Localitate
        self.company_address_street = sdenumire_Strada + ' ' + snumar_Strada
        self.company_address_details = sdetalii_Adresa
        self.company_vat_status = scpTVA
        self.company_vat_number = "RO" + str(cui) if scpTVA else None

    def __repr__(self):
        return (f"CompanyInfo(nrRegCom={self.company_registration_number}, cui={self.company_tin}, "
                f"denumire={self.company_name}, "
                f"denumire_Strada={self.company_address_street}, "
                f"denumire_Judet={self.company_address_country_subentity}, "
                f" cod_Judet={self.company_address_country_subentity_code}, "
                f"denumire_Localitate={self.company_address_city}, "
                f"cpTVA={self.company_vat_status}, "
                f"vat_number={self.company_vat_number})")

def get_company_based_on_CUI(cui):
    url = "https://api.speedsoft.ro/dbapi.php"
    payload = f'cui_client=123456789&api_key=0f831e68512865df443fae53ff38947ab25c65d7127f4c983844c2e85e0cd59c&cui={cui}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    nrRegCom = data["data"]["date_generale"]["nrRegCom"]
    cui = data["data"]["date_generale"]["cui"]
    denumire = data["data"]["date_generale"]["denumire"]

    sdenumire_Strada = data["data"]["adresa_sediu_social"]["sdenumire_Strada"]
    snumar_Strada = data["data"]["adresa_sediu_social"]["snumar_Strada"]
    sdenumire_Judet = data["data"]["adresa_sediu_social"]["sdenumire_Judet"]
    scod_JudetAuto = data["data"]["adresa_sediu_social"]["scod_JudetAuto"]
    sdenumire_Localitate = data["data"]["adresa_sediu_social"]["sdenumire_Localitate"]
    sdetalii_Adresa = data["data"]["adresa_sediu_social"]["sdetalii_Adresa"]

    scpTVA = data["data"]["inregistrare_scop_Tva"]["scpTVA"]

    company_info = CompanyInfo(nrRegCom, cui, denumire, sdenumire_Strada, snumar_Strada, sdenumire_Judet, scod_JudetAuto, sdenumire_Localitate, scpTVA, sdetalii_Adresa)
    
    return company_info
