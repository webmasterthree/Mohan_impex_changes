import frappe

def import_all_companies():
    companies = [
        {
            "company_name": "BIKANERVALA FOODS PVT. LTD",
            "abbr": "BIKANERVALA FOODS PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "BIMBO BAKERIES INDIA PVT.LTD",
            "abbr": "BIMBO BAKERIES INDIA PVT.LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "BIMBO BAKERIES INDIA PVT.LTD - NOIDA",
            "abbr": "BIMBO BAKERIES INDIA PVT.LTD - NOIDA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "BIMBO BAKERIES INDIA PVT.LTD - SONIPAT",
            "abbr": "BIMBO BAKERIES INDIA PVT.LTD - SONIPAT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "DHARAMPAL PREMCHAND LTD (DS GROUP)",
            "abbr": "DHARAMPAL PREMCHAND LTD (DS GROUP)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "HECTOR BEVERAGES PVT LTD",
            "abbr": "HECTOR BEVERAGES PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "HECTOR BEVERAGES PVT LTD - MYSORE",
            "abbr": "HECTOR BEVERAGES PVT LTD - MYSORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S PIONEER SALES AGENCY",
            "abbr": "M/S PIONEER SALES AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI233",
            "default_currency": "INR"
        },
        {
            "company_name": "MODERN FOOD ENTERPRISES PVT.LTD - MUMBAI",
            "abbr": "MODERN FOOD ENTERPRISES PVT.LTD - MUMBAI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "NIF PRIVATE LIMITED",
            "abbr": "NIF PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "READY ROTI INDIA PVT. LTD - (CHP)",
            "abbr": "READY ROTI INDIA PVT. LTD - (CHP)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "READY ROTI INDIA PVT. LTD - (SKD)",
            "abbr": "READY ROTI INDIA PVT. LTD - (SKD)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "READY ROTI INDIA PVT. LTD - GREATER NOIDA",
            "abbr": "READY ROTI INDIA PVT. LTD - GREATER NOIDA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "Sabharwal Food industries Pvt Ltd",
            "abbr": "Sabharwal Food industries Pvt Ltd",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "KOHINOOR BISCUIT PRODUCTS",
            "abbr": "KOHINOOR BISCUIT PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI128",
            "default_currency": "INR"
        },
        {
            "company_name": "A R ENTERPRISES",
            "abbr": "A R ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ACME PAINTS & RESIN PRIVATE LIMITED",
            "abbr": "ACME PAINTS & RESIN PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AGARWAL CHEMICALS",
            "abbr": "AGARWAL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AGARWAL PLASTICS",
            "abbr": "AGARWAL PLASTICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "AGASTYA BHANDAR",
            "abbr": "AGASTYA BHANDAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "AGRIM CHEMTECH",
            "abbr": "AGRIM CHEMTECH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "AGRO-TECH(INDIA)",
            "abbr": "AGRO-TECH(INDIA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AHMEDABAD CHEMICAL COMPANY",
            "abbr": "AHMEDABAD CHEMICAL COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "AJAY TRADING CORPORATION",
            "abbr": "AJAY TRADING CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AJSP EXIM",
            "abbr": "AJSP EXIM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ALPHA PHARMA",
            "abbr": "ALPHA PHARMA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AMBICA CHEMICAL & INDUSTRIAL CORPORATION",
            "abbr": "AMBICA CHEMICAL & INDUSTRIAL CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "AMRUTA TRADERS",
            "abbr": "AMRUTA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ANCHAL BHANDER",
            "abbr": "ANCHAL BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ANGEL CHEMICALS",
            "abbr": "ANGEL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ANKIT ENTERPRISE",
            "abbr": "ANKIT ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "APEX AGENCIES",
            "abbr": "APEX AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ARORA BROTHERS",
            "abbr": "ARORA BROTHERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AROTI FOODS",
            "abbr": "AROTI FOODS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ARTI ENTERPRISES",
            "abbr": "ARTI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ARUN COMMERCIAL COMPANY",
            "abbr": "ARUN COMMERCIAL COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ARUN ENTERPRISES",
            "abbr": "ARUN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "ARVIND INDUSTRIALS",
            "abbr": "ARVIND INDUSTRIALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ASIAN DISTRIBUTION TRADE CORPORATION",
            "abbr": "ASIAN DISTRIBUTION TRADE CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AVERY CHEMICALS",
            "abbr": "AVERY CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "AYUSH KUMAR JAIN",
            "abbr": "AYUSH KUMAR JAIN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "B D1958 AND CO",
            "abbr": "B D1958 AND CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BABU LAL GUPTA & CO",
            "abbr": "BABU LAL GUPTA & CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BAJAJ ALCHEM PVT. LTD",
            "abbr": "BAJAJ ALCHEM PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERS POINT - KOL",
            "abbr": "BAKERS POINT - KOL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BALAJEE IMPEX",
            "abbr": "BALAJEE IMPEX",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BALAJI ADHESIVE",
            "abbr": "BALAJI ADHESIVE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BALAJI POLYPACK",
            "abbr": "BALAJI POLYPACK",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BASANT TRADERS",
            "abbr": "BASANT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BENGAL ESSENCE STORE ( Kolkata )",
            "abbr": "BENGAL ESSENCE STORE ( Kolkata )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BENGAL POLITHENE",
            "abbr": "BENGAL POLITHENE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BERLCHEM  PRIVATE LTD.",
            "abbr": "BERLCHEM  PRIVATE LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BHAGWATI ENTERPRISE",
            "abbr": "BHAGWATI ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BHARAT HEAVY CHEMICALS",
            "abbr": "BHARAT HEAVY CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BHARTI CHEMICALS",
            "abbr": "BHARTI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BIHANI CHEMICAL INDUSTRIES (P) LTD.",
            "abbr": "BIHANI CHEMICAL INDUSTRIES (P) LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BISWANATH HALDER",
            "abbr": "BISWANATH HALDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BLG PRODUCTS PVT LTD",
            "abbr": "BLG PRODUCTS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BNM ORGANICS (P) LTD",
            "abbr": "BNM ORGANICS (P) LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "BONGFAB INTERNATIONAL",
            "abbr": "BONGFAB INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "BUDGE BUDGE REFINERIES LIMITED",
            "abbr": "BUDGE BUDGE REFINERIES LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CALCUTTA  BAKERY",
            "abbr": "CALCUTTA  BAKERY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CALCUTTA CHEMSALES CORPORATION",
            "abbr": "CALCUTTA CHEMSALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CALCUTTA COLOUR COMPANY.",
            "abbr": "CALCUTTA COLOUR COMPANY.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CARMELO LALOO",
            "abbr": "CARMELO LALOO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CENTURY CHEMICAL",
            "abbr": "CENTURY CHEMICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHAMPION COLOUR UDYOG",
            "abbr": "CHAMPION COLOUR UDYOG",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDA DEVI TRADING CO",
            "abbr": "CHANDA DEVI TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDRESH AGENCY",
            "abbr": "CHANDRESH AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEM TRADE",
            "abbr": "CHEM TRADE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMBAZER INDUSTRIES",
            "abbr": "CHEMBAZER INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMI COLOUR RESINS",
            "abbr": "CHEMI COLOUR RESINS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMICAL TRADERS",
            "abbr": "CHEMICAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMICALS ( INDIA ) COMPANY",
            "abbr": "CHEMICALS ( INDIA ) COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMI-CULTURE",
            "abbr": "CHEMI-CULTURE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMPURE INTERNATIONAL",
            "abbr": "CHEMPURE INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMTEX SPECIALITY LIMITED",
            "abbr": "CHEMTEX SPECIALITY LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHEMUNICATION ENTERPRISE",
            "abbr": "CHEMUNICATION ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "CHHEDILAL SHAW AND SONS",
            "abbr": "CHHEDILAL SHAW AND SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "CHIRANJIT KARAN",
            "abbr": "CHIRANJIT KARAN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DANG PHARMACEUTICALS",
            "abbr": "DANG PHARMACEUTICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DAS ENTERPRISES",
            "abbr": "DAS ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DASHAKARMA BHANDAR",
            "abbr": "DASHAKARMA BHANDAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DAYA SALES",
            "abbr": "DAYA SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DEBRAJ NAYAK",
            "abbr": "DEBRAJ NAYAK",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DEEPAK ENTERPRISE",
            "abbr": "DEEPAK ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DELHI PETRO CHEMICALS CO.",
            "abbr": "DELHI PETRO CHEMICALS CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DEZINER",
            "abbr": "DEZINER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DNV FOOD PRODUCTS PVT LTD",
            "abbr": "DNV FOOD PRODUCTS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DOSHI BROTHERS",
            "abbr": "DOSHI BROTHERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DUTSON ENTERPRISES",
            "abbr": "DUTSON ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "DUTTA ENTERPRISE",
            "abbr": "DUTTA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "DUTTSINHA & CO.",
            "abbr": "DUTTSINHA & CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "EAST INDIA TRADE CORPORATION",
            "abbr": "EAST INDIA TRADE CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ECHEM CORP (NEW)",
            "abbr": "ECHEM CORP (NEW)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "EVERLIGHT INTERNATIONAL",
            "abbr": "EVERLIGHT INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Excel Orgo-Chem Private Limited",
            "abbr": "Excel Orgo-Chem Private Limited",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "EXEMPLAR CHEMICALS LTD.",
            "abbr": "EXEMPLAR CHEMICALS LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Exim Incorporation",
            "abbr": "Exim Incorporation",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "FITNESS GALAXY TRADERS",
            "abbr": "FITNESS GALAXY TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "G P JEWELLERY TOOLS",
            "abbr": "G P JEWELLERY TOOLS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "G. P. TRADERS",
            "abbr": "G. P. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "G.M.P. TRADERS",
            "abbr": "G.M.P. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GAIA BIOTECH",
            "abbr": "GAIA BIOTECH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GANPATI INTERNATIONAL",
            "abbr": "GANPATI INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GAYATRI & SONS",
            "abbr": "GAYATRI & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GEE-TEE CHEMICALS",
            "abbr": "GEE-TEE CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GENERAL SUPPLY CORPORATION",
            "abbr": "GENERAL SUPPLY CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GHOSH BROTHERS FOOD PRODUCTS",
            "abbr": "GHOSH BROTHERS FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GIRDHARI CHEMICALS & RESINS PVT LTD",
            "abbr": "GIRDHARI CHEMICALS & RESINS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GIRDHARI LAL & SONS",
            "abbr": "GIRDHARI LAL & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GITA INDUSTRIES",
            "abbr": "GITA INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GK ENTERPRISE",
            "abbr": "GK ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GLOBAL CHEMICALS LIMITED",
            "abbr": "GLOBAL CHEMICALS LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GLOBAL FLAVOURS AND INGREDIENTS PRIVATE LIMITED",
            "abbr": "GLOBAL FLAVOURS AND INGREDIENTS PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GLOBAL MARKETING SERVICE",
            "abbr": "GLOBAL MARKETING SERVICE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GOBINDRAM JESSARAM",
            "abbr": "GOBINDRAM JESSARAM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GOGJI GROCERRS",
            "abbr": "GOGJI GROCERRS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GOLDEN TRADING CO",
            "abbr": "GOLDEN TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GRASS GROUP",
            "abbr": "GRASS GROUP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "GT JAYANTI AGROCHEM (INDIA) PRIVATE LIMITED",
            "abbr": "GT JAYANTI AGROCHEM (INDIA) PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "GUPTA TARDERS",
            "abbr": "GUPTA TARDERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "HARI SADHAN DEY  GRANDSONS",
            "abbr": "HARI SADHAN DEY  GRANDSONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "HIRA LABORATORY & INDUSTRIAL CHEMICALS",
            "abbr": "HIRA LABORATORY & INDUSTRIAL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "HI-TECH MINERALS & CHEMICALS",
            "abbr": "HI-TECH MINERALS & CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "HOWRAH CHEMICAL WORKS",
            "abbr": "HOWRAH CHEMICAL WORKS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "IN ESSENCE  (GOBINDRAM JESSARAM)",
            "abbr": "IN ESSENCE  (GOBINDRAM JESSARAM)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "INDUSTRIAL  CHEMICAL CONCERN",
            "abbr": "INDUSTRIAL  CHEMICAL CONCERN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "INTERNATIONAL TRADERS",
            "abbr": "INTERNATIONAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ISHIKA ENTERPRISE",
            "abbr": "ISHIKA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "J.C.B ORGO CHEM & MINERALS (CLOSSED)",
            "abbr": "J.C.B ORGO CHEM & MINERALS (CLOSSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "J.C.B ORGO CHEM & MINERALS (NEW)",
            "abbr": "J.C.B ORGO CHEM & MINERALS (NEW)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "J.J GROUP",
            "abbr": "J.J GROUP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "J.K. CHEMICAL",
            "abbr": "J.K. CHEMICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "J.K.CHEMICALS ( Bagmari )",
            "abbr": "J.K.CHEMICALS ( Bagmari )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "JAYANTA SAHA",
            "abbr": "JAYANTA SAHA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "JECO AGROVET PRIVATE LIMITED",
            "abbr": "JECO AGROVET PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "JEECON FOODS PRIVATE LIMITED",
            "abbr": "JEECON FOODS PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "JINEN CHEMICALS",
            "abbr": "JINEN CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "JOY KALI BHANDER",
            "abbr": "JOY KALI BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "JUTIFY LIFESTYLE PVT LTD",
            "abbr": "JUTIFY LIFESTYLE PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "JYOTI INTERNATIONAL",
            "abbr": "JYOTI INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "K V ENTERPRISES PVT LTD (JALANDHAR)",
            "abbr": "K V ENTERPRISES PVT LTD (JALANDHAR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "K V ENTERPRISES PVT LTD (LUDHIANA)",
            "abbr": "K V ENTERPRISES PVT LTD (LUDHIANA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "K. MADHUSUDAN & CO",
            "abbr": "K. MADHUSUDAN & CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "KARAN TIE UP PRIVATE LIMITED",
            "abbr": "KARAN TIE UP PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "KAVITA ENTERPRISES",
            "abbr": "KAVITA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "KB MASALE",
            "abbr": "KB MASALE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Khicha Inorganic Chemicals",
            "abbr": "Khicha Inorganic Chemicals",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "KING CHEMICALS",
            "abbr": "KING CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "KINJAL INTERNATIONAL",
            "abbr": "KINJAL INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "KIRTI CHEMICAL",
            "abbr": "KIRTI CHEMICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "KNP ENTERPRISE",
            "abbr": "KNP ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "KRUTI ENTERPRISES",
            "abbr": "KRUTI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "KUNAL CHEMICALS",
            "abbr": "KUNAL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "LAB CHEM CORPORATION",
            "abbr": "LAB CHEM CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "LAXMINARAYAN GHISURAM",
            "abbr": "LAXMINARAYAN GHISURAM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "LOK  CHEMICALS  PVT LTD",
            "abbr": "LOK  CHEMICALS  PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "LOKENATH ENTERPRISES",
            "abbr": "LOKENATH ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "LUXMI COSMETICS",
            "abbr": "LUXMI COSMETICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "LYKIS LIMITED",
            "abbr": "LYKIS LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M J TRADING",
            "abbr": "M J TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M. B. D. & COMPANY",
            "abbr": "M. B. D. & COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M. KANTILAL & CO",
            "abbr": "M. KANTILAL & CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M.G.COMPANY",
            "abbr": "M.G.COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M.S.GHOSH BROTHERS FRUIT PRODUCTS",
            "abbr": "M.S.GHOSH BROTHERS FRUIT PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S  SUPER FOODS",
            "abbr": "M/S  SUPER FOODS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S D. S. CHEMICAL CONCERN",
            "abbr": "M/S D. S. CHEMICAL CONCERN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S D.L.PHARMA",
            "abbr": "M/S D.L.PHARMA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S DEEKAY FOODS AND CHEMICALS",
            "abbr": "M/S DEEKAY FOODS AND CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S EKAAYAA INDIA",
            "abbr": "M/S EKAAYAA INDIA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S HIMANSHU EXIM",
            "abbr": "M/S HIMANSHU EXIM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S MAA KALI BHANDAR",
            "abbr": "M/S MAA KALI BHANDAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S NIRMESH ENTERPRISES PVT.LTD.",
            "abbr": "M/S NIRMESH ENTERPRISES PVT.LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S RAJATH CONSUMABLES",
            "abbr": "M/S RAJATH CONSUMABLES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S S F TRADERS",
            "abbr": "M/S S F TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. B. R. PETROCHEM PVT LTD",
            "abbr": "M/S. B. R. PETROCHEM PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. BANERJEE FOOD – AID COMPANY",
            "abbr": "M/S. BANERJEE FOOD – AID COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S.R.K.ENTERPRISES",
            "abbr": "M/S.R.K.ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA KALI CHEMICALS",
            "abbr": "MAA KALI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MAGNUM SURGICAL",
            "abbr": "MAGNUM SURGICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MAHALAXMI MALT PRODUCTS PVT LTD",
            "abbr": "MAHALAXMI MALT PRODUCTS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MAHESH COMMERCIAL ENTERPRISES",
            "abbr": "MAHESH COMMERCIAL ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MAHESH ENTERPRISE",
            "abbr": "MAHESH ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MAJI & SONS",
            "abbr": "MAJI & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MANAS GARAI",
            "abbr": "MANAS GARAI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MANASHI CHEMICALS",
            "abbr": "MANASHI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MANIBHADRA FOOD PRODUCTS",
            "abbr": "MANIBHADRA FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MANINUL HAQUE SEIKH",
            "abbr": "MANINUL HAQUE SEIKH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MANJUSHREE ENTERPRISE",
            "abbr": "MANJUSHREE ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MARUTI ENTERPRISES",
            "abbr": "MARUTI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MAYA DEVI KHERWAR",
            "abbr": "MAYA DEVI KHERWAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MEGHNIL CHEMICALS",
            "abbr": "MEGHNIL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MEHTA MADICARE PVT LTD",
            "abbr": "MEHTA MADICARE PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MEHTA TRADING CO",
            "abbr": "MEHTA TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MICRO  VET",
            "abbr": "MICRO  VET",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MINERVA BIOGENIX PVT LTD",
            "abbr": "MINERVA BIOGENIX PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MIVON CHEMICALS",
            "abbr": "MIVON CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MODIT TRADERS",
            "abbr": "MODIT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MONOHAR LAL COMPANY",
            "abbr": "MONOHAR LAL COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MRK CHEMICALS",
            "abbr": "MRK CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "MSAS AGRO PRIVATE LIMITED",
            "abbr": "MSAS AGRO PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "MURARI STORES",
            "abbr": "MURARI STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "N D M  H BIOORGANICS LLP",
            "abbr": "N D M  H BIOORGANICS LLP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "N.C.CHEMICALS",
            "abbr": "N.C.CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NABANU DEBSHARMA",
            "abbr": "NABANU DEBSHARMA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NADEEM ANWAR",
            "abbr": "NADEEM ANWAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "NARESH AGENCIES",
            "abbr": "NARESH AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "NARESH CHEMICALS",
            "abbr": "NARESH CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NAROTTAMDAS AND COMPANY",
            "abbr": "NAROTTAMDAS AND COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "NARSINGH FOOD PRODUCTS",
            "abbr": "NARSINGH FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NASIR ALI KHAN",
            "abbr": "NASIR ALI KHAN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NATIONAL TRADING COMPANY",
            "abbr": "NATIONAL TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NAVEEN ENTERPRISE",
            "abbr": "NAVEEN ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NEMI CHAND NIRMAL KUMAR",
            "abbr": "NEMI CHAND NIRMAL KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NETAI DEY",
            "abbr": "NETAI DEY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW GUPTA PRODUCTS",
            "abbr": "NEW GUPTA PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "NIRVVAN LIFESCIENCE PRIVATE LIMITED",
            "abbr": "NIRVVAN LIFESCIENCE PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "NOVA CHEMICALS",
            "abbr": "NOVA CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "OMARHAM ENTERPRISES PRIVATE LIMITED",
            "abbr": "OMARHAM ENTERPRISES PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "OZONE POLYFORM PVT. LTD.",
            "abbr": "OZONE POLYFORM PVT. LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "P.K. TRADING",
            "abbr": "P.K. TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "P.K.ENTERPRISE",
            "abbr": "P.K.ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "P.S. SOHAN SINGH",
            "abbr": "P.S. SOHAN SINGH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PALAN HALDER",
            "abbr": "PALAN HALDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PANKAJ DYES & CHEMICALS",
            "abbr": "PANKAJ DYES & CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PANKAJ TRADERS",
            "abbr": "PANKAJ TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PARAS DYES & CHEMICALS",
            "abbr": "PARAS DYES & CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PAREKH CHEM PRODUCTS INDIA",
            "abbr": "PAREKH CHEM PRODUCTS INDIA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PARESH DATTO",
            "abbr": "PARESH DATTO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PAWAN CHEMICALS",
            "abbr": "PAWAN CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PHARMACHEM TRADERS PVT LTD",
            "abbr": "PHARMACHEM TRADERS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PIYUSH TRADING CO.",
            "abbr": "PIYUSH TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PK TAPES",
            "abbr": "PK TAPES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PRAGATI SOLUTIONS",
            "abbr": "PRAGATI SOLUTIONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PRECIOUS CHEMICALS",
            "abbr": "PRECIOUS CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PREM CHAND & SONS",
            "abbr": "PREM CHAND & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PRIME CHEMICALS",
            "abbr": "PRIME CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PRIMETECH CORPORATION",
            "abbr": "PRIMETECH CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PRIMUS CORPORATION",
            "abbr": "PRIMUS CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "PRITAM MANNA",
            "abbr": "PRITAM MANNA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PUNAM ENTERPRISE",
            "abbr": "PUNAM ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "PUSKAR TRADECOM PVT. LTD",
            "abbr": "PUSKAR TRADECOM PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "QUAKER CHEMICAL INDIA PRIVATE LIMITED",
            "abbr": "QUAKER CHEMICAL INDIA PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "R K FOODS",
            "abbr": "R K FOODS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "R.D.CHEM",
            "abbr": "R.D.CHEM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "R.S. TRADERS (WAYLINK)",
            "abbr": "R.S. TRADERS (WAYLINK)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RABINDRANATH DAS BAIRAGYA",
            "abbr": "RABINDRANATH DAS BAIRAGYA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RADHA RANI EXPORTS",
            "abbr": "RADHA RANI EXPORTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RADIANT SALES",
            "abbr": "RADIANT SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RADIANT SALES",
            "abbr": "RADIANT SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RAGA INTERNATIONAL",
            "abbr": "RAGA INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJ KUMAR SAW",
            "abbr": "RAJ KUMAR SAW",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Rajesh Sales Agencies",
            "abbr": "Rajesh Sales Agencies",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RAMA SUGAR",
            "abbr": "RAMA SUGAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RAMKRISHNA ENTERPRISE",
            "abbr": "RAMKRISHNA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RANENDU BERA",
            "abbr": "RANENDU BERA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RANJEET SAW",
            "abbr": "RANJEET SAW",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RATHI INDUSTRIES",
            "abbr": "RATHI INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RELIABLE AGENCIES",
            "abbr": "RELIABLE AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RELIABLE SUPPLIERS",
            "abbr": "RELIABLE SUPPLIERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RIDDHI AROMATICS",
            "abbr": "RIDDHI AROMATICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RIDDHI CHEMICALS",
            "abbr": "RIDDHI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RIYA ORGANICS",
            "abbr": "RIYA ORGANICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "RIZWAN ANSAARI",
            "abbr": "RIZWAN ANSAARI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "ROYS FOOD PRODUCTS",
            "abbr": "ROYS FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RUDRA CHEMICALS",
            "abbr": "RUDRA CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "RUPALI ENTERPRISES",
            "abbr": "RUPALI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "S M ICECREAM  MART",
            "abbr": "S M ICECREAM  MART",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "S S ENTERPRISES",
            "abbr": "S S ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "S.B. TRADERS",
            "abbr": "S.B. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "S.J.CHEMICALS PVT. LTD",
            "abbr": "S.J.CHEMICALS PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "S.K.MINERALS AGENCIES PVT. LTD.",
            "abbr": "S.K.MINERALS AGENCIES PVT. LTD.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SAMIR AGENCIES",
            "abbr": "SAMIR AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SANJAY TEXTILES",
            "abbr": "SANJAY TEXTILES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SANKET TRADERS",
            "abbr": "SANKET TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SARAOGI INDUSTRIES",
            "abbr": "SARAOGI INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SARVODAYA CHEMICAL",
            "abbr": "SARVODAYA CHEMICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SAURABH MARKETING",
            "abbr": "SAURABH MARKETING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHAKTI BIOFUEL",
            "abbr": "SHAKTI BIOFUEL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIV CHEMCORP",
            "abbr": "SHIV CHEMCORP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIV DURGA CHEMICAL ENTERPRISE",
            "abbr": "SHIV DURGA CHEMICAL ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIVA CHEMICALS",
            "abbr": "SHIVA CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE BHARAT TRADING CORPORATION",
            "abbr": "SHREE BHARAT TRADING CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE DEV UDYOG",
            "abbr": "SHREE DEV UDYOG",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE FOOD PRODUCT",
            "abbr": "SHREE FOOD PRODUCT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE JEE TRADING CO.",
            "abbr": "SHREE JEE TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE OM TRADERS",
            "abbr": "SHREE OM TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Shree Parasnath Hi-Strength Chemical Resources",
            "abbr": "Shree Parasnath Hi-Strength Chemical Resources",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE PAWANPUTRA ENTERPRISE",
            "abbr": "SHREE PAWANPUTRA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE SHANKAR BHANDER",
            "abbr": "SHREE SHANKAR BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREEJI PHARMA CHEM",
            "abbr": "SHREEJI PHARMA CHEM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Shreekhetra Sea Shell",
            "abbr": "Shreekhetra Sea Shell",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "Shri Gopal Trading Company",
            "abbr": "Shri Gopal Trading Company",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHUBH CHEM(INDIA)",
            "abbr": "SHUBH CHEM(INDIA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHUBHANKAR BISWAS",
            "abbr": "SHUBHANKAR BISWAS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SHYAM SALES",
            "abbr": "SHYAM SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SIDDHI VINAYAK TRADERS",
            "abbr": "SIDDHI VINAYAK TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SINGHANIA ENTERPRISES",
            "abbr": "SINGHANIA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SKYSCRAPERS CHEMEX PRIVATE LIMITED",
            "abbr": "SKYSCRAPERS CHEMEX PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SONU & COMPANY",
            "abbr": "SONU & COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SOUTH INDIA SALES CORPORATION",
            "abbr": "SOUTH INDIA SALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SOVA CHEMICALS CO",
            "abbr": "SOVA CHEMICALS CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SPA INTERNATIONAL",
            "abbr": "SPA INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SPECIALTY CHEMICALS  POLYMERS (KOLKATA)",
            "abbr": "SPECIALTY CHEMICALS  POLYMERS (KOLKATA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SPH CHEMICALS",
            "abbr": "SPH CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SREE RAM SATYA PRAKASH",
            "abbr": "SREE RAM SATYA PRAKASH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SREEMAA STORES",
            "abbr": "SREEMAA STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI PADMAVATHI POLYCHEM PVT LTD",
            "abbr": "SRI PADMAVATHI POLYCHEM PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "STERLITE CHEMICALS",
            "abbr": "STERLITE CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SUNIL CHEMICALS",
            "abbr": "SUNIL CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SUPERBHA & SONS",
            "abbr": "SUPERBHA & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SURAJ ENTERPRISE",
            "abbr": "SURAJ ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SURANA SPICES SUPPLY AGENCIES",
            "abbr": "SURANA SPICES SUPPLY AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SURENDRA CHEMICALS & INDUSTRIES",
            "abbr": "SURENDRA CHEMICALS & INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "SWAN INTERNATIONAL",
            "abbr": "SWAN INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "SWASTIK ENTERPRISES",
            "abbr": "SWASTIK ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TARA MAA CHEMICALS & COMPANY",
            "abbr": "TARA MAA CHEMICALS & COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TARA MAA TRADING CO",
            "abbr": "TARA MAA TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "TEXCHEM (INDIA)",
            "abbr": "TEXCHEM (INDIA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "THAKUR  CO",
            "abbr": "THAKUR  CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "THE POPULAR CHEMICAL WORKS",
            "abbr": "THE POPULAR CHEMICAL WORKS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "THE SCIENTIFIC & CHEMICAL PRODUCTS PVT. LTD",
            "abbr": "THE SCIENTIFIC & CHEMICAL PRODUCTS PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TIDE SALES CORPORATION",
            "abbr": "TIDE SALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TIRUPATI CHEMICAL COMPANY",
            "abbr": "TIRUPATI CHEMICAL COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TOOLSCO",
            "abbr": "TOOLSCO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "TOOLSCO (NEW)",
            "abbr": "TOOLSCO (NEW)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "TRIPOOT INDIA PVT LTD",
            "abbr": "TRIPOOT INDIA PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "TRIVENI OIL INDUSTRIES",
            "abbr": "TRIVENI OIL INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "UMA CHEMICALS",
            "abbr": "UMA CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "UMA INDUSTRIES",
            "abbr": "UMA INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "UNICHEM",
            "abbr": "UNICHEM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "UNITED TRADING CO",
            "abbr": "UNITED TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "V3S FOODS & BEVERAGES PVT. LTD",
            "abbr": "V3S FOODS & BEVERAGES PVT. LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VARIETY STORES (EZRA STREET)",
            "abbr": "VARIETY STORES (EZRA STREET)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "VENKATESH CHEMICALS",
            "abbr": "VENKATESH CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VIBGYOR CHEMICALS",
            "abbr": "VIBGYOR CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VIJAY TRADING CO",
            "abbr": "VIJAY TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "VINAYAKA VENTURES",
            "abbr": "VINAYAKA VENTURES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "VIRAJ INDUSTRIES",
            "abbr": "VIRAJ INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VISHAL CHEM (INDIA)",
            "abbr": "VISHAL CHEM (INDIA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VISHNU CORPORATION",
            "abbr": "VISHNU CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VISHNU TRADE CENTRE",
            "abbr": "VISHNU TRADE CENTRE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "VITARICH AGRO FOOD INDIA LIMITED",
            "abbr": "VITARICH AGRO FOOD INDIA LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "WAYLINK INTERNATIONAL",
            "abbr": "WAYLINK INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI206",
            "default_currency": "INR"
        },
        {
            "company_name": "WELL TRADE CHEMICALS",
            "abbr": "WELL TRADE CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "YES ENTERPRISE",
            "abbr": "YES ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI250",
            "default_currency": "INR"
        },
        {
            "company_name": "3A Corporation",
            "abbr": "3A Corporation",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "A J ENTERPRISES",
            "abbr": "A J ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "A K ESSENCE",
            "abbr": "A K ESSENCE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "A R SALES AND SERVICES (A R ENTER)",
            "abbr": "A R SALES AND SERVICES (A R ENTER)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "A TO Z AQUA RAITU BAZAR",
            "abbr": "A TO Z AQUA RAITU BAZAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "A V N Enterprises",
            "abbr": "A V N Enterprises",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "A. M. STORES",
            "abbr": "A. M. STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "A.F. STORE",
            "abbr": "A.F. STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "AADEEP TRADERS",
            "abbr": "AADEEP TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "AB EXIM",
            "abbr": "AB EXIM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ABHAY ENTERPRISES",
            "abbr": "ABHAY ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ADARSH TRADERS",
            "abbr": "ADARSH TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "AGARWAL TRADERS",
            "abbr": "AGARWAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "AGARWAL TRADERS",
            "abbr": "AGARWAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "AHK ENTERPRISE",
            "abbr": "AHK ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "AJAY CHEMICALS",
            "abbr": "AJAY CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ALOK ENTERPRISES - (UMESH KUMAR)",
            "abbr": "ALOK ENTERPRISES - (UMESH KUMAR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ALOKA AGENCY",
            "abbr": "ALOKA AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "AMAL KUMAR DEY",
            "abbr": "AMAL KUMAR DEY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "AMAL MAJUMDAR",
            "abbr": "AMAL MAJUMDAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "AMAL TRADERS",
            "abbr": "AMAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "AMARNATH REFRIGERATION",
            "abbr": "AMARNATH REFRIGERATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "AMBIKA ENTERPRISES",
            "abbr": "AMBIKA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "AMIT PLASTIC CENTER (BAKERY & PLASTIC)",
            "abbr": "AMIT PLASTIC CENTER (BAKERY & PLASTIC)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ANKIT TRADERS",
            "abbr": "ANKIT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ANUP KUMAR & SONS",
            "abbr": "ANUP KUMAR & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ANUP KUMAR-ARRAH",
            "abbr": "ANUP KUMAR-ARRAH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "APNA KIRANA",
            "abbr": "APNA KIRANA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ARIHANT PACKAGING",
            "abbr": "ARIHANT PACKAGING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "ARUNACHAL FOOD PRODUCTS",
            "abbr": "ARUNACHAL FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "ASHARAM MASTERFOOD STORES",
            "abbr": "ASHARAM MASTERFOOD STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "ASSOCIATED DYES & CHEMICALS",
            "abbr": "ASSOCIATED DYES & CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "AYUSH ENTERPRISE",
            "abbr": "AYUSH ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "B P MARKETING  (Dhanbad)",
            "abbr": "B P MARKETING  (Dhanbad)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "B.G. TRADERS",
            "abbr": "B.G. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "B.K. SUPPLIER'S",
            "abbr": "B.K. SUPPLIER'S",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "B.K. SUPPLIER'S",
            "abbr": "B.K. SUPPLIER'S",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "B.L WIRE PRODUCTS",
            "abbr": "B.L WIRE PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "B.M.ENTERPRISES",
            "abbr": "B.M.ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "B.M.ENTERPRISES",
            "abbr": "B.M.ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "BABA AGENCIES",
            "abbr": "BABA AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "BABA LOKENATH BAKERY STORE",
            "abbr": "BABA LOKENATH BAKERY STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BABLU BAKERY ENTERPRISES",
            "abbr": "BABLU BAKERY ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BADAM AGENCIES",
            "abbr": "BADAM AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKED MART",
            "abbr": "BAKED MART",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERS CHOICE",
            "abbr": "BAKERS CHOICE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKER'S HOME",
            "abbr": "BAKER'S HOME",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERS POINT",
            "abbr": "BAKERS POINT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERY & VARIETY STORE",
            "abbr": "BAKERY & VARIETY STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERY AND VARIETY STORES (CLOSED)",
            "abbr": "BAKERY AND VARIETY STORES (CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERY HOUSE(DALSINGH SARAI)",
            "abbr": "BAKERY HOUSE(DALSINGH SARAI)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERY HOUSE(DALSINGH SARAI)",
            "abbr": "BAKERY HOUSE(DALSINGH SARAI)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKERY STORES (DHANBAD)",
            "abbr": "BAKERY STORES (DHANBAD)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "BAKSHI TRADERS  - SITAMADHI",
            "abbr": "BAKSHI TRADERS  - SITAMADHI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BALAJI AGENCIES",
            "abbr": "BALAJI AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI245",
            "default_currency": "INR"
        },
        {
            "company_name": "BALAJI ENTERPRISES (RANCHI  )",
            "abbr": "BALAJI ENTERPRISES (RANCHI  )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "BALMIKI CHOUDHARY",
            "abbr": "BALMIKI CHOUDHARY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BAMBAM KIRANA STORE (PIRO)",
            "abbr": "BAMBAM KIRANA STORE (PIRO)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "BANSAL TRADERS",
            "abbr": "BANSAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "BARNALA PLSTIC & PLASTIC ZONE",
            "abbr": "BARNALA PLSTIC & PLASTIC ZONE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "BHAGWATI TRADING -CHHAPRA",
            "abbr": "BHAGWATI TRADING -CHHAPRA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "BHARAT GENERAL STORES",
            "abbr": "BHARAT GENERAL STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "BHARAT TRADERS",
            "abbr": "BHARAT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "BHARAT TRADERS",
            "abbr": "BHARAT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "BHASKARA SAI CHEMICALS",
            "abbr": "BHASKARA SAI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "BIKI STORE",
            "abbr": "BIKI STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "BLISVEL FOODS PRIVATE LIMITED",
            "abbr": "BLISVEL FOODS PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "BUNTI ENTERPRISE",
            "abbr": "BUNTI ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "CHAITANYA AQUA NEEDS",
            "abbr": "CHAITANYA AQUA NEEDS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "CHAKKA RANGA RAO SON",
            "abbr": "CHAKKA RANGA RAO SON",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANCHAL PROSAD JAISWAL",
            "abbr": "CHANCHAL PROSAD JAISWAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDA PROVISION STORE",
            "abbr": "CHANDA PROVISION STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDAN KUMAR - NAWADA",
            "abbr": "CHANDAN KUMAR - NAWADA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDAN KUMAR (SALES)",
            "abbr": "CHANDAN KUMAR (SALES)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "CHANDRIKA YAADAV",
            "abbr": "CHANDRIKA YAADAV",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "CHINTU BAKERY",
            "abbr": "CHINTU BAKERY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "CHIRAG TRADING COMPANY",
            "abbr": "CHIRAG TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "CHITTURI CHINNA PITCHAIAH TRADERS",
            "abbr": "CHITTURI CHINNA PITCHAIAH TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "CHOUDHARY HARDWARE",
            "abbr": "CHOUDHARY HARDWARE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "CHOWDHURY HARDWARE & ICE CREAM MATERIALS",
            "abbr": "CHOWDHURY HARDWARE & ICE CREAM MATERIALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "CHOWMAN HOSPITALITY PRIVATE LIMITED",
            "abbr": "CHOWMAN HOSPITALITY PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "D. ENTERPRISES",
            "abbr": "D. ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "D.S. TRADERS",
            "abbr": "D.S. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "D.S.S.&SONS",
            "abbr": "D.S.S.&SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "DADI MAA KRIPA ENTERPRISES",
            "abbr": "DADI MAA KRIPA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "DAYARAM KHATIK  SONS",
            "abbr": "DAYARAM KHATIK  SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "DEEPAK KUMAR AGARWAL",
            "abbr": "DEEPAK KUMAR AGARWAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "DHANESH TRADE INDIA",
            "abbr": "DHANESH TRADE INDIA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "Dhanraj Agarwal (NEW GST)",
            "abbr": "Dhanraj Agarwal (NEW GST)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "DHAR BROTHERS",
            "abbr": "DHAR BROTHERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "DIN DAYAL MUDI BHANDER",
            "abbr": "DIN DAYAL MUDI BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "DIUS FOODS & FLIPS PRIVATE LIMITED",
            "abbr": "DIUS FOODS & FLIPS PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "DIVYAAHAR AGRO PRODUCTS PVT LTD",
            "abbr": "DIVYAAHAR AGRO PRODUCTS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "DOZEN BAKE FARM",
            "abbr": "DOZEN BAKE FARM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "DSN TRADERS",
            "abbr": "DSN TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "FASHION HUB & SAHU STORES",
            "abbr": "FASHION HUB & SAHU STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "FRIENDS ENTERPRISE",
            "abbr": "FRIENDS ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "FRIENDS ENTERPRISE",
            "abbr": "FRIENDS ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "FRONTIER FRUIT STORES",
            "abbr": "FRONTIER FRUIT STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "FUTURE TREDLINGS",
            "abbr": "FUTURE TREDLINGS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "GA GUPTA STORE",
            "abbr": "GA GUPTA STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "GANAPATI UDYOG",
            "abbr": "GANAPATI UDYOG",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "GAURAV ENTERPRISES(Jay Prakash Mondal)",
            "abbr": "GAURAV ENTERPRISES(Jay Prakash Mondal)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "GD TRADERS",
            "abbr": "GD TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "GEETA BTRADE",
            "abbr": "GEETA BTRADE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "GHOSH ENTERPRISE",
            "abbr": "GHOSH ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "GITA PRINTING HOUSE",
            "abbr": "GITA PRINTING HOUSE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "GMKR FOOD WORLD LLP",
            "abbr": "GMKR FOOD WORLD LLP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "GOLDEN REFRIGERATION-BHAGALPUR",
            "abbr": "GOLDEN REFRIGERATION-BHAGALPUR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "GOUTAM ROY (MAA SARODA STORE A/C)",
            "abbr": "GOUTAM ROY (MAA SARODA STORE A/C)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "GOYAL TRADING CO.",
            "abbr": "GOYAL TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "GUPTA TRADERS",
            "abbr": "GUPTA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "GYAN PRAKASH",
            "abbr": "GYAN PRAKASH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "HANUMAN AGENCY (PUPRI)",
            "abbr": "HANUMAN AGENCY (PUPRI)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "HARI OM TRADERS",
            "abbr": "HARI OM TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "HEMANT KUMAR JOSHI",
            "abbr": "HEMANT KUMAR JOSHI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "HIND CHEM",
            "abbr": "HIND CHEM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "HIND TRADERS",
            "abbr": "HIND TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "HINDUSTAN TRADERS (HAJIPUR)",
            "abbr": "HINDUSTAN TRADERS (HAJIPUR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "HIRA ENTERPRISE",
            "abbr": "HIRA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "I NARAYANAN NAIR",
            "abbr": "I NARAYANAN NAIR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "I.F.F.D.C KRISHI SEWA KENDRA",
            "abbr": "I.F.F.D.C KRISHI SEWA KENDRA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ICON TRADING COMPNAY",
            "abbr": "ICON TRADING COMPNAY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "INDIA TRADERS",
            "abbr": "INDIA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "INDUSHREE ORGANIC",
            "abbr": "INDUSHREE ORGANIC",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "ISHIKA ENTERPRISES",
            "abbr": "ISHIKA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "J P STORES",
            "abbr": "J P STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "JAI BHAVANI TRADERS",
            "abbr": "JAI BHAVANI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "JAI MATA DI TRADING",
            "abbr": "JAI MATA DI TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "JAI SANTHOSHIMATHA TRADERS",
            "abbr": "JAI SANTHOSHIMATHA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "JAIN TOYS",
            "abbr": "JAIN TOYS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "JAISWAL  TRADING",
            "abbr": "JAISWAL  TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "JAISWAL SALES (Jharkhand)",
            "abbr": "JAISWAL SALES (Jharkhand)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "JAISWAL STEEL WORKS",
            "abbr": "JAISWAL STEEL WORKS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "JAMUN SAH ZARIBUTI",
            "abbr": "JAMUN SAH ZARIBUTI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "JAYA TRADING COMPANY",
            "abbr": "JAYA TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "JAYASHREE ENTERPRISE (DEBABRATA ROY)",
            "abbr": "JAYASHREE ENTERPRISE (DEBABRATA ROY)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "JAYSHREE TRADING",
            "abbr": "JAYSHREE TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "JHARNA STORES",
            "abbr": "JHARNA STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "JOY GURU STORE (BASIRHAT)",
            "abbr": "JOY GURU STORE (BASIRHAT)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "JOYGURU STORES (MURSHIDABAD)",
            "abbr": "JOYGURU STORES (MURSHIDABAD)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "JUHI STORES",
            "abbr": "JUHI STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "JVR SCIENTIFIC COMPANY",
            "abbr": "JVR SCIENTIFIC COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "K S DISTRIBUTORS",
            "abbr": "K S DISTRIBUTORS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KAMADHENU KIRANA & GENERAL STORES",
            "abbr": "KAMADHENU KIRANA & GENERAL STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "KAMAL STORES ( Dhanbad)",
            "abbr": "KAMAL STORES ( Dhanbad)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "KAMALA DEVI",
            "abbr": "KAMALA DEVI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "KAMALALAYA AGENCIES",
            "abbr": "KAMALALAYA AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "KARTICK ADHIKARY (FROZEN TREATS)",
            "abbr": "KARTICK ADHIKARY (FROZEN TREATS)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KATHIKAA FOOD INGREDIENTS",
            "abbr": "KATHIKAA FOOD INGREDIENTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "KAUSHIK ENTERPRISE",
            "abbr": "KAUSHIK ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "KAZI  FOOD PRODUCT",
            "abbr": "KAZI  FOOD PRODUCT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "KAZI PLASTIC HOUSE",
            "abbr": "KAZI PLASTIC HOUSE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "KEDIA TRADERS",
            "abbr": "KEDIA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KHANDELWAL TRADERS",
            "abbr": "KHANDELWAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "KIRAN TRADERS",
            "abbr": "KIRAN TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "KOLKATA_ORCHID_ONLINE",
            "abbr": "KOLKATA_ORCHID_ONLINE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KRISHNA TRADERS (Kolkata)",
            "abbr": "KRISHNA TRADERS (Kolkata)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KRISHNAA ENTERPRISES(CLOSED)",
            "abbr": "KRISHNAA ENTERPRISES(CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "KUMAR ENTERPRISES",
            "abbr": "KUMAR ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "KUMKUM DEVI",
            "abbr": "KUMKUM DEVI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "KUNDU BROTHER'S",
            "abbr": "KUNDU BROTHER'S",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "KV CITRUS BIOTECH",
            "abbr": "KV CITRUS BIOTECH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "L.N. TRADERS",
            "abbr": "L.N. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "LAKHI BHANDAR",
            "abbr": "LAKHI BHANDAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "LAKSHMI INDUSTRIES",
            "abbr": "LAKSHMI INDUSTRIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "LAXMI NARAYAN BAKERY STORE",
            "abbr": "LAXMI NARAYAN BAKERY STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "LAXMINARAYAN SANDEEP KUMAR",
            "abbr": "LAXMINARAYAN SANDEEP KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "M R GENERIC FOODS PRIVATE LIMITED",
            "abbr": "M R GENERIC FOODS PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M. P. SALES CORPORATION",
            "abbr": "M. P. SALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI192",
            "default_currency": "INR"
        },
        {
            "company_name": "M. P. SALES CORPORATION",
            "abbr": "M. P. SALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI192",
            "default_currency": "INR"
        },
        {
            "company_name": "M.R. DISTRIBUTORS",
            "abbr": "M.R. DISTRIBUTORS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S . STAR SALES CORPORATION (ABDUL MANNAN)",
            "abbr": "M/S . STAR SALES CORPORATION (ABDUL MANNAN)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S . STAR SALES CORPORATION (ABDUL MANNAN)",
            "abbr": "M/S . STAR SALES CORPORATION (ABDUL MANNAN)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S A K ENTERPRISE",
            "abbr": "M/S A K ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S AGARWAL PACKWELL CORPORATION",
            "abbr": "M/S AGARWAL PACKWELL CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S AGRAWAL TRADING (Closed)",
            "abbr": "M/S AGRAWAL TRADING (Closed)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S AMAN ENTERPRISES",
            "abbr": "M/S AMAN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/s ARIF PLASTIC AGENCY",
            "abbr": "M/s ARIF PLASTIC AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S BAKER''S SOLUTION",
            "abbr": "M/S BAKER''S SOLUTION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S BAKERY PRODUCT",
            "abbr": "M/S BAKERY PRODUCT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S BALAJI TRADERS",
            "abbr": "M/S BALAJI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S BLB FOODS",
            "abbr": "M/S BLB FOODS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S CHAUDHARY STORES",
            "abbr": "M/S CHAUDHARY STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S GOPAL PRASAD",
            "abbr": "M/S GOPAL PRASAD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S HYACINTH PRODUCTS LLP",
            "abbr": "M/S HYACINTH PRODUCTS LLP",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S JAI MAA MANGALA TRADERS",
            "abbr": "M/S JAI MAA MANGALA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S JAIN TRADERS",
            "abbr": "M/S JAIN TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S KAMAL KUMAR JAIN",
            "abbr": "M/S KAMAL KUMAR JAIN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S KANYAKA TRADERS PROP SMT TAVVA VARALAKSHMI",
            "abbr": "M/S KANYAKA TRADERS PROP SMT TAVVA VARALAKSHMI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S KISHORE TRADERS",
            "abbr": "M/S KISHORE TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S KOLKATA BAKERY & PLASTIC",
            "abbr": "M/S KOLKATA BAKERY & PLASTIC",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S L.K. TRADERS",
            "abbr": "M/S L.K. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S LAKSHMI SAI ENTERPRISES",
            "abbr": "M/S LAKSHMI SAI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S LIFE TRADERS (Star Bakery)",
            "abbr": "M/S LIFE TRADERS (Star Bakery)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S LIFE TRADERS (Star Bakery)",
            "abbr": "M/S LIFE TRADERS (Star Bakery)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S MAHAKAL ENTERPRISES",
            "abbr": "M/S MAHAKAL ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S MANOKAMNA TRADERS",
            "abbr": "M/S MANOKAMNA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S MUSKAN ENTERPRISES",
            "abbr": "M/S MUSKAN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S NANDLAL BAJRANGLAL",
            "abbr": "M/S NANDLAL BAJRANGLAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S PAPPU STORE",
            "abbr": "M/S PAPPU STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S PRAKASH STORE",
            "abbr": "M/S PRAKASH STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S PRASAD SALES AGENCY",
            "abbr": "M/S PRASAD SALES AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S RAHUL  RUDRA ENTERPRISES",
            "abbr": "M/S RAHUL  RUDRA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S RAMKRISHNA TRADING",
            "abbr": "M/S RAMKRISHNA TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S S K ENTERPRISES",
            "abbr": "M/S S K ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S S R ENTERPRISES",
            "abbr": "M/S S R ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SANGMA STORES",
            "abbr": "M/S SANGMA STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SATYA FOODS PRODUCT",
            "abbr": "M/S SATYA FOODS PRODUCT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SHARDA TRADERS(Closed)",
            "abbr": "M/S SHARDA TRADERS(Closed)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SOUMITRA PAUL",
            "abbr": "M/S SOUMITRA PAUL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SOUMITRA PAUL",
            "abbr": "M/S SOUMITRA PAUL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "M/s SREE SITA RAMANJANEYA PROVISIONS",
            "abbr": "M/s SREE SITA RAMANJANEYA PROVISIONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S STAR MARKETING",
            "abbr": "M/S STAR MARKETING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S STAR MARKETING",
            "abbr": "M/S STAR MARKETING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S SWASTIK REFRIGERATION",
            "abbr": "M/S SWASTIK REFRIGERATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/s THAKURMAL VADHWANI",
            "abbr": "M/s THAKURMAL VADHWANI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S TIRUMULA ENTERPRISES",
            "abbr": "M/S TIRUMULA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S V.S. FROZEN FOODS",
            "abbr": "M/S V.S. FROZEN FOODS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. ANJALI STORES ( Babu Nag)",
            "abbr": "M/S. ANJALI STORES ( Babu Nag)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. ANKIT MARKETING    TRADERSS(NO BILLING)",
            "abbr": "M/S. ANKIT MARKETING    TRADERSS(NO BILLING)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. ARPITA ENTERPRISE",
            "abbr": "M/S. ARPITA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. BHAWANI ENTERPRISES",
            "abbr": "M/S. BHAWANI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. D. S. TRADERS",
            "abbr": "M/S. D. S. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. J.S. STORES",
            "abbr": "M/S. J.S. STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. LAXMI VARIETIES AND FOOD PRODUCTS",
            "abbr": "M/S. LAXMI VARIETIES AND FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. NATIONAL BAKERY HOUSE",
            "abbr": "M/S. NATIONAL BAKERY HOUSE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S. URMISON FOOD PRODUCTS",
            "abbr": "M/S. URMISON FOOD PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S.ANNAPURNA BHANDER",
            "abbr": "M/S.ANNAPURNA BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S.ANNAPURNA BHANDER",
            "abbr": "M/S.ANNAPURNA BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S.DURGA PRASAD TIBRIWAL",
            "abbr": "M/S.DURGA PRASAD TIBRIWAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "M/S.SHIVA ENTERPRISE - Sanjay Kr.Gupta",
            "abbr": "M/S.SHIVA ENTERPRISE - Sanjay Kr.Gupta",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA BHAVANI SALES",
            "abbr": "MAA BHAVANI SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI245",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA KRISHNA ENTERPRISE (CLOSED)",
            "abbr": "MAA KRISHNA ENTERPRISE (CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA LAXMI ESSENCE STORE (SAMIR KUMAR MONDAL)",
            "abbr": "MAA LAXMI ESSENCE STORE (SAMIR KUMAR MONDAL)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA MANASA STORE",
            "abbr": "MAA MANASA STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA MANSHA BHANDER (Ashoknagar)",
            "abbr": "MAA MANSHA BHANDER (Ashoknagar)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA PATNESHWARI TRADERS (NEW GST)",
            "abbr": "MAA PATNESHWARI TRADERS (NEW GST)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA SARADA ENTERPRISE",
            "abbr": "MAA SARADA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA SARODA STORE",
            "abbr": "MAA SARODA STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA SHANTI TRADERS",
            "abbr": "MAA SHANTI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA TARA ENTERPRISES(CLOSSED)",
            "abbr": "MAA TARA ENTERPRISES(CLOSSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA TARA OIL SHOP (W.E.F. 01/12/20)",
            "abbr": "MAA TARA OIL SHOP (W.E.F. 01/12/20)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MAA YOGESHVARI TRADERS",
            "abbr": "MAA YOGESHVARI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "MAGADH BAKERY STORE",
            "abbr": "MAGADH BAKERY STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MAHAKAL ENTERPRISES",
            "abbr": "MAHAKAL ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "MAHAVIR SPICES  DRY FRUITS",
            "abbr": "MAHAVIR SPICES  DRY FRUITS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "MAJUMDER BAKE CHEMICALS",
            "abbr": "MAJUMDER BAKE CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MAJUMDER TRADERS",
            "abbr": "MAJUMDER TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MAMONI STORE ( MURSHIDABAD )",
            "abbr": "MAMONI STORE ( MURSHIDABAD )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "MANGAL STORE",
            "abbr": "MANGAL STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MANGALAM ENTERPRISES",
            "abbr": "MANGALAM ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MARUTI HANUMAN REFRIGERATION",
            "abbr": "MARUTI HANUMAN REFRIGERATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MATRI TRADING CO.",
            "abbr": "MATRI TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "MAYA DEVI",
            "abbr": "MAYA DEVI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "MD. KHALID ANSARI",
            "abbr": "MD. KHALID ANSARI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MD.SAKEEL - ARRAH",
            "abbr": "MD.SAKEEL - ARRAH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "MIDNAPUR BAKERY CENTRE",
            "abbr": "MIDNAPUR BAKERY CENTRE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MILLENIUM EXIM PRIVATE LIMITED",
            "abbr": "MILLENIUM EXIM PRIVATE LIMITED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "MOHIT TRADERS-BHAGALPUR",
            "abbr": "MOHIT TRADERS-BHAGALPUR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "MOTHER INDIA CONSUMER PRODUCTS",
            "abbr": "MOTHER INDIA CONSUMER PRODUCTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "MOTHER TRADERS",
            "abbr": "MOTHER TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "MP CHEM",
            "abbr": "MP CHEM",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "MUNNA KUMAR",
            "abbr": "MUNNA KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "N STAR BAKERY",
            "abbr": "N STAR BAKERY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "NABARATAN KUMAR (CLOSED)",
            "abbr": "NABARATAN KUMAR (CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "NANTU ENTERPRISE",
            "abbr": "NANTU ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "NARAIN DAS CHATURBHUJ DAS",
            "abbr": "NARAIN DAS CHATURBHUJ DAS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "Narayan Bakary & Food Products",
            "abbr": "Narayan Bakary & Food Products",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "NATH BAKERY STORE (New)",
            "abbr": "NATH BAKERY STORE (New)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "NAVYA SAI TRADERS",
            "abbr": "NAVYA SAI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "NEMAT KARIM STORE",
            "abbr": "NEMAT KARIM STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW AGRAWAL TRADERS",
            "abbr": "NEW AGRAWAL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW BISHWAKARMA ENTERPRISE - CLOSED",
            "abbr": "NEW BISHWAKARMA ENTERPRISE - CLOSED",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW GHOSH STORE",
            "abbr": "NEW GHOSH STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW HAJI STORE",
            "abbr": "NEW HAJI STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW MANU VARIETY STORES",
            "abbr": "NEW MANU VARIETY STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW OM BAKERY & SONS",
            "abbr": "NEW OM BAKERY & SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "NEW VARIETY STORES (FALTA)",
            "abbr": "NEW VARIETY STORES (FALTA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "NIRMAL KUMAR GAIRA",
            "abbr": "NIRMAL KUMAR GAIRA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "NIRMALA TRADERS(CLOSED)",
            "abbr": "NIRMALA TRADERS(CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "NX MERCHANTS",
            "abbr": "NX MERCHANTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "OM AGENCY",
            "abbr": "OM AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "OM ENTERPRISES (NAGPUR UNIT)",
            "abbr": "OM ENTERPRISES (NAGPUR UNIT)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI245",
            "default_currency": "INR"
        },
        {
            "company_name": "OM TRADERS",
            "abbr": "OM TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ORIENT REFRIGERATION  & ENGINEERING CO.",
            "abbr": "ORIENT REFRIGERATION  & ENGINEERING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "OVEN GALLERY",
            "abbr": "OVEN GALLERY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "P K KIRANA (NEW)",
            "abbr": "P K KIRANA (NEW)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "PAL CHOWDHURY BROTHERS",
            "abbr": "PAL CHOWDHURY BROTHERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "PAL ENTERPRISE",
            "abbr": "PAL ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "PAPPU BAKERY STORES (MANOJ KR GUPTA)",
            "abbr": "PAPPU BAKERY STORES (MANOJ KR GUPTA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "PAPPU REFRIGERATION",
            "abbr": "PAPPU REFRIGERATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "PAVAN KUMAR  CO",
            "abbr": "PAVAN KUMAR  CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "PLASTIC DUKAN",
            "abbr": "PLASTIC DUKAN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "PODDAR BROTHERS (MURSHIDABAD)",
            "abbr": "PODDAR BROTHERS (MURSHIDABAD)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "PRAKASH ENTERPRISES",
            "abbr": "PRAKASH ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "PRAKASH REFRIGERATION",
            "abbr": "PRAKASH REFRIGERATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "PRAPTI ENTERPRISES",
            "abbr": "PRAPTI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "PRASANTA BANIK",
            "abbr": "PRASANTA BANIK",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "PRASHANT TRADERS",
            "abbr": "PRASHANT TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "PRASHANT TRADERS ( Anirudh Chowdhary)",
            "abbr": "PRASHANT TRADERS ( Anirudh Chowdhary)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "PREETI FLAVOUR & FRAGRANCE",
            "abbr": "PREETI FLAVOUR & FRAGRANCE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "PRISHA ENTERPRISES (NEW)",
            "abbr": "PRISHA ENTERPRISES (NEW)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "PROSENJIT SAHA",
            "abbr": "PROSENJIT SAHA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "PULAK SAHA",
            "abbr": "PULAK SAHA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "PURAVI MARKETTING",
            "abbr": "PURAVI MARKETTING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "QUICK SERVICE",
            "abbr": "QUICK SERVICE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "R.L.ENTERPRISES",
            "abbr": "R.L.ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "RADHE VARIETY STORE",
            "abbr": "RADHE VARIETY STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RAHUL TRADERS",
            "abbr": "RAHUL TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJ AGENCIES",
            "abbr": "RAJ AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJ AGENCIES (VIJAYWADA)",
            "abbr": "RAJ AGENCIES (VIJAYWADA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJ ESSENCE STORE",
            "abbr": "RAJ ESSENCE STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJ ESSENCE STORES",
            "abbr": "RAJ ESSENCE STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJESH KUMAR",
            "abbr": "RAJESH KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJESWARI DISTRIBUTORS",
            "abbr": "RAJESWARI DISTRIBUTORS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJIV KUMAR ( Samastipur )",
            "abbr": "RAJIV KUMAR ( Samastipur )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJIV KUMAR ( Samastipur )",
            "abbr": "RAJIV KUMAR ( Samastipur )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJMITHRA AGENCIES",
            "abbr": "RAJMITHRA AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAJU GENERAL STORE",
            "abbr": "RAJU GENERAL STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAMCHANDRA RANGWALE",
            "abbr": "RAMCHANDRA RANGWALE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RAMDEV TRADERS (VIJAYWADA)",
            "abbr": "RAMDEV TRADERS (VIJAYWADA)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "RAMRAJ STORES",
            "abbr": "RAMRAJ STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RANJAN KUMAR SINGH(CLOSED)",
            "abbr": "RANJAN KUMAR SINGH(CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RANJEET TRADING COMPANY",
            "abbr": "RANJEET TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "RAUSHAN KUMAR",
            "abbr": "RAUSHAN KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "RAVEENDRA COMMERCIAL CORPORATION",
            "abbr": "RAVEENDRA COMMERCIAL CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "REFRIGERATING MACHINERY MART",
            "abbr": "REFRIGERATING MACHINERY MART",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "RISE AND SHINE",
            "abbr": "RISE AND SHINE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "RISHABH ENTERPRISES",
            "abbr": "RISHABH ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI192",
            "default_currency": "INR"
        },
        {
            "company_name": "RJD ENTERPRISE",
            "abbr": "RJD ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "ROHIT TRADERS -CHHAPRA",
            "abbr": "ROHIT TRADERS -CHHAPRA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "ROMY ENTERPRISE",
            "abbr": "ROMY ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ROSHAN TRADERS",
            "abbr": "ROSHAN TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "ROY BROTHER",
            "abbr": "ROY BROTHER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "ROY TRADERS",
            "abbr": "ROY TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "ROY TRADERS - (CLOSED)",
            "abbr": "ROY TRADERS - (CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "RRR ENTERPRISES",
            "abbr": "RRR ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "RRR ENTERPRISES",
            "abbr": "RRR ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "RUDRA TRADING CO.",
            "abbr": "RUDRA TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "S AGENCIES",
            "abbr": "S AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "S K SCIENTIFIC TRADERS",
            "abbr": "S K SCIENTIFIC TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "S M FOOD INGREDIENTS",
            "abbr": "S M FOOD INGREDIENTS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "S M TRADERS",
            "abbr": "S M TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI256",
            "default_currency": "INR"
        },
        {
            "company_name": "S P B ENTERPRISES",
            "abbr": "S P B ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "S R TRADING CO.",
            "abbr": "S R TRADING CO.",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "S S ENTERPRISE (CHANDANNAGAR)",
            "abbr": "S S ENTERPRISE (CHANDANNAGAR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "S S R STORES",
            "abbr": "S S R STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "S. H. TRADING",
            "abbr": "S. H. TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "S.K. TRADERS",
            "abbr": "S.K. TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "S.K.TRADERS (HAJIPUR)",
            "abbr": "S.K.TRADERS (HAJIPUR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "S.KUMAR TENT HOUSE",
            "abbr": "S.KUMAR TENT HOUSE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SADHUKHAN TRADING COMPANY",
            "abbr": "SADHUKHAN TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SAHA ENTERPRISE",
            "abbr": "SAHA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SAHA ENTERPRISE",
            "abbr": "SAHA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SAHA ENTERPRISE (CLOSED)",
            "abbr": "SAHA ENTERPRISE (CLOSED)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SAI CHEMICALS",
            "abbr": "SAI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SAI FOOD PRODUCTS (BHAGALPUR)",
            "abbr": "SAI FOOD PRODUCTS (BHAGALPUR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SAI LAKSHMI ENTERPRISES",
            "abbr": "SAI LAKSHMI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SAI RAJ TRADERS",
            "abbr": "SAI RAJ TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SAI TEJA ENTERPRISES",
            "abbr": "SAI TEJA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SALIN ENTERPRISES",
            "abbr": "SALIN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "SALONI ENTERPRISES",
            "abbr": "SALONI ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SALUJA STORE ( TATANAGAR)",
            "abbr": "SALUJA STORE ( TATANAGAR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SALUJA STORES (BIHAR UNIT )",
            "abbr": "SALUJA STORES (BIHAR UNIT )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SAMAN CHEMICALS",
            "abbr": "SAMAN CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "SAMAN CHEMICALS",
            "abbr": "SAMAN CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "SANDEEP TRADERS",
            "abbr": "SANDEEP TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SANTOSH KIRANA STORE",
            "abbr": "SANTOSH KIRANA STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SARAOGI TRADERS",
            "abbr": "SARAOGI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "SASI PROVISIONS",
            "abbr": "SASI PROVISIONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SATYANARAYAN  KISHAN KUMAR",
            "abbr": "SATYANARAYAN  KISHAN KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "SATYANARAYAN LAGANAUTI STORE",
            "abbr": "SATYANARAYAN LAGANAUTI STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SATYAWATI TRADERS",
            "abbr": "SATYAWATI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHAGUN FOOD PRODUCT",
            "abbr": "SHAGUN FOOD PRODUCT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHAMBHU REFRIGRATION",
            "abbr": "SHAMBHU REFRIGRATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHANMUKHA ENTERPRISES",
            "abbr": "SHANMUKHA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SHANTI TRADERS",
            "abbr": "SHANTI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SHARDA SALES CORPORATION",
            "abbr": "SHARDA SALES CORPORATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIBAM ENTERPRISE",
            "abbr": "SHIBAM ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SHILLONG ESSENCE HOUSE",
            "abbr": "SHILLONG ESSENCE HOUSE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIMLA TRADERS  - SIWAN",
            "abbr": "SHIMLA TRADERS  - SIWAN",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIV SHAKTI TRADERS",
            "abbr": "SHIV SHAKTI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIV SHAKTI TRADING",
            "abbr": "SHIV SHAKTI TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SHIVA TRADERS",
            "abbr": "SHIVA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHRADHA GENERAL STORE (Dumka)",
            "abbr": "SHRADHA GENERAL STORE (Dumka)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE BALAJI TRADING & AGENCIES",
            "abbr": "SHREE BALAJI TRADING & AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE KRISHNA BAKERY",
            "abbr": "SHREE KRISHNA BAKERY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE SHYAM COMMUNICATION",
            "abbr": "SHREE SHYAM COMMUNICATION",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE SHYAM MARKETING",
            "abbr": "SHREE SHYAM MARKETING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE STORE (MUNGER)",
            "abbr": "SHREE STORE (MUNGER)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREE VINAYAK ENTERPRISES",
            "abbr": "SHREE VINAYAK ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SHREYA STORE",
            "abbr": "SHREYA STORE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SHRI CHANDRA TRADERS",
            "abbr": "SHRI CHANDRA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SHRI RAM TRADERS",
            "abbr": "SHRI RAM TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "SHRI SHYAM SALES (RANCHI )",
            "abbr": "SHRI SHYAM SALES (RANCHI )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SHUBHAM TRADING",
            "abbr": "SHUBHAM TRADING",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SHYAM ZARIBUTTI",
            "abbr": "SHYAM ZARIBUTTI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SIDDHIVINAYAK SALES",
            "abbr": "SIDDHIVINAYAK SALES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "SIROMONI FOOD PRODUCTS PVT.LTD",
            "abbr": "SIROMONI FOOD PRODUCTS PVT.LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SOHAM RAJ TRADERS",
            "abbr": "SOHAM RAJ TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "SOMYA ENTERPRISES",
            "abbr": "SOMYA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SONAM INTERNATIONAL",
            "abbr": "SONAM INTERNATIONAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "SONU KUMAR",
            "abbr": "SONU KUMAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SONU KUMAR GUPTA",
            "abbr": "SONU KUMAR GUPTA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SPELL FOOD CHEMICALS PVT LTD",
            "abbr": "SPELL FOOD CHEMICALS PVT LTD",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI147",
            "default_currency": "INR"
        },
        {
            "company_name": "SREEDHARALA JOGA RAO &SONS",
            "abbr": "SREEDHARALA JOGA RAO &SONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SREEKRISHNA BHANDER",
            "abbr": "SREEKRISHNA BHANDER",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI ASHOKA ENTERPRISES",
            "abbr": "SRI ASHOKA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI BALAJI CHEMICALS",
            "abbr": "SRI BALAJI CHEMICALS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI KAMAKSHI TRADERS",
            "abbr": "SRI KAMAKSHI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI KANAKADURGA GAS CYLINDERS SUPPLYING COMPANY",
            "abbr": "SRI KANAKADURGA GAS CYLINDERS SUPPLYING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI KESHAV TRADERS",
            "abbr": "SRI KESHAV TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI LALITHA TRADERS",
            "abbr": "SRI LALITHA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI MA ENTERPRISE",
            "abbr": "SRI MA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI MAHABIR CHEMICAL",
            "abbr": "SRI MAHABIR CHEMICAL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI MURALI KRISHNA COLOUR COMPANY",
            "abbr": "SRI MURALI KRISHNA COLOUR COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI MYTREYA GENERAL STORES",
            "abbr": "SRI MYTREYA GENERAL STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI MYTREYA GENERAL STORES",
            "abbr": "SRI MYTREYA GENERAL STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI NAKODA ENTERPRISES",
            "abbr": "SRI NAKODA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI NAMBURU SAMBASIVA RAO",
            "abbr": "SRI NAMBURU SAMBASIVA RAO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI SAI SRINIVASA PROVISIONS",
            "abbr": "SRI SAI SRINIVASA PROVISIONS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI SAI STORE ( BIHAR )",
            "abbr": "SRI SAI STORE ( BIHAR )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI SRI KASI VISALAKSHI GENERAL STORES",
            "abbr": "SRI SRI KASI VISALAKSHI GENERAL STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI VIJAYADURGA TRADERS",
            "abbr": "SRI VIJAYADURGA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SRI VINAYAKA TRADERS",
            "abbr": "SRI VINAYAKA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "STAR AGENCY ( Darbhanga )",
            "abbr": "STAR AGENCY ( Darbhanga )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "STAR AGENCY ( Darbhanga )",
            "abbr": "STAR AGENCY ( Darbhanga )",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "STAR AGENCY (MOTIHARI)",
            "abbr": "STAR AGENCY (MOTIHARI)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "STAR AGENCY (MUZAFFARPUR)",
            "abbr": "STAR AGENCY (MUZAFFARPUR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SUBHA ENTERPRISE",
            "abbr": "SUBHA ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI077",
            "default_currency": "INR"
        },
        {
            "company_name": "SUBRAMANYESWARA TRADERS",
            "abbr": "SUBRAMANYESWARA TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SUDHANSHU KIRANA AND GENERAL STORE -BEGUSARAI",
            "abbr": "SUDHANSHU KIRANA AND GENERAL STORE -BEGUSARAI",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "SUGANDH TRADE CENTRE",
            "abbr": "SUGANDH TRADE CENTRE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SUJOY BHAKAT",
            "abbr": "SUJOY BHAKAT",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "SUMIT ENTERPRISE",
            "abbr": "SUMIT ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "SUNAMI TRADERS",
            "abbr": "SUNAMI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SUNDARBAN AQUA FEED CENTRE",
            "abbr": "SUNDARBAN AQUA FEED CENTRE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "SUNIL KUMAR BILLA",
            "abbr": "SUNIL KUMAR BILLA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "SWAASTHYUM ENTERPRISES",
            "abbr": "SWAASTHYUM ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI192",
            "default_currency": "INR"
        },
        {
            "company_name": "SWATHI AGENCIES",
            "abbr": "SWATHI AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "SWEET INDIA",
            "abbr": "SWEET INDIA",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "T K ENTERPRISE (PAKUR)",
            "abbr": "T K ENTERPRISE (PAKUR)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "TAMANNA ENTERPRISES",
            "abbr": "TAMANNA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "TAPAS ENTERPRISE",
            "abbr": "TAPAS ENTERPRISE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "TARUN KUMAR SARKAR",
            "abbr": "TARUN KUMAR SARKAR",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "TARUN PLASTIC STORES",
            "abbr": "TARUN PLASTIC STORES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "TARUN TRADERS",
            "abbr": "TARUN TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "TAWHEED & BROTHERS",
            "abbr": "TAWHEED & BROTHERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "THE ARYAN ENTERPRISES",
            "abbr": "THE ARYAN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "THE RK CREAM CAVE",
            "abbr": "THE RK CREAM CAVE",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "TIGRANIA TRADING COMPANY",
            "abbr": "TIGRANIA TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
        {
            "company_name": "UMAPATI TRADERS",
            "abbr": "UMAPATI TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "UMESH SINGH",
            "abbr": "UMESH SINGH",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "UNITED FOODS & ORGANICS",
            "abbr": "UNITED FOODS & ORGANICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "UPHAR GALAXY",
            "abbr": "UPHAR GALAXY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "USHA STORES (Malda)",
            "abbr": "USHA STORES (Malda)",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI079",
            "default_currency": "INR"
        },
        {
            "company_name": "UTTAM PAUL",
            "abbr": "UTTAM PAUL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "UTTAM PAUL",
            "abbr": "UTTAM PAUL",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI135",
            "default_currency": "INR"
        },
        {
            "company_name": "V.V.ORGANICS",
            "abbr": "V.V.ORGANICS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI227",
            "default_currency": "INR"
        },
        {
            "company_name": "VAISHNAVI RUPA AGENCY",
            "abbr": "VAISHNAVI RUPA AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "VARAD TRADERS",
            "abbr": "VARAD TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "VED KIRANA & TRADING CO",
            "abbr": "VED KIRANA & TRADING CO",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "VENKATA RAMANA ENTERPRISES",
            "abbr": "VENKATA RAMANA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "VENKATESWARA KIRANA AND DRY FRUITS",
            "abbr": "VENKATESWARA KIRANA AND DRY FRUITS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "VERMA ENTERPRISES",
            "abbr": "VERMA ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI243",
            "default_currency": "INR"
        },
        {
            "company_name": "VIJAY INTERPRISES",
            "abbr": "VIJAY INTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "VIRAAT AGENCY",
            "abbr": "VIRAAT AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "VIRAAT AGENCY",
            "abbr": "VIRAAT AGENCY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI223",
            "default_currency": "INR"
        },
        {
            "company_name": "VIRAJ TRADERS",
            "abbr": "VIRAJ TRADERS",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "VIVEK ENTERPRISES",
            "abbr": "VIVEK ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "VIVEK ENTERPRISES",
            "abbr": "VIVEK ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI150",
            "default_currency": "INR"
        },
        {
            "company_name": "YASH TRADING COMPANY",
            "abbr": "YASH TRADING COMPANY",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI210",
            "default_currency": "INR"
        },
        {
            "company_name": "YASIN ENTERPRISES",
            "abbr": "YASIN ENTERPRISES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI252",
            "default_currency": "INR"
        },
        {
            "company_name": "UNIVERSAL AGENCIES",
            "abbr": "UNIVERSAL AGENCIES",
            "company_type": "Channel Partner",
            "custom_company_type": "Channel Partner",
            "default_source_warehouse": "DNK WAREHOUSE - MISL",
            "employee": "MI067",
            "default_currency": "INR"
        },
    ]

    for company in companies:
        if frappe.db.exists("Company", company["company_name"]):
            print(f"⏩ Skipping existing: {company['company_name']}")
            continue
        frappe.get_doc({"doctype": "Company", **company}).insert()
    frappe.db.commit()
    print("✅ All companies inserted successfully.")