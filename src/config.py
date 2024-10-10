import random
from utils import calculate_iban_control_digits, generate_spanish_dni, generate_password

# List of municipalities in the Basque Country
cities = [
    # Bizkaia
    "Bilbao", "Barakaldo", "Getxo", "Portugalete", "Santurtzi", "Basauri", "Leioa", 
    "Galdakao", "Sestao", "Durango", "Erandio", "Bermeo", "Mungia", "Sopela", "Berango",
    # Gipuzkoa
    "Donostia", "Irun", "Errenteria", "Eibar", "Zarautz", "Arrasate", 
    "Hernani", "Lasarte-Oria", "Hondarribia", "Pasaia", "Andoain",
    # Araba
    "Vitoria-Gasteiz", "Llodio", "Amurrio", "Salvatierra/Agurain", "Oyón-Oion", 
    "Iruña de Oca", "Alegría-Dulantzi", "Zuia", "Labastida", "Elciego"
]

buyer_profiles = {
    #   'buyer_0': {
    #     'name': 'Luis',
    #     'surname': 'Garay',
    #     'city': 'Bilbao',
    #     'birth_date': '1996-08-10',
    #     'initial_assets': (1000, 1000),
    #     'salary': (100, 1000),
    #     'has_partner': False,
    #     'partner_works': False,
    #     'children': 0,
    #     'owns_house': False,
    #     'has_car': False,
    #     'index_fix_expenses': 1,
    #     'index_var_expenses': 1,
    # },
    'buyer_1': {
        'name': 'Luis',
        'surname': 'Garay',
        'city': 'Bilbao',
        'birth_date': '1996-08-10',
        'initial_assets': (3000, 5000),
        'salary': (500, 3000),
        'has_partner': False,
        'partner_works': False,
        'children': 0,
        'owns_house': False,
        'has_car': True,
        'index_fix_expenses': 1,
        'index_var_expenses': 0.9,

    },
    'buyer_2': {
        'name': 'Carmen',
        'surname': 'Lozano',
        'city': 'Zarautz',
        'birth_date': '1984-09-05',
        'initial_assets': (1000, 12000),
        'salary': (1900, 2000),
        'has_partner': False,
        'partner_works': False,
        'children': 2,
        'owns_house': True,
        'has_car': False,
        'index_fix_expenses': 1,
        'index_var_expenses': 1.1,
    },
    'buyer_3': {
        'name': 'Ana',
        'surname': 'Piñeiro',
        'city': 'Amurrio',
        'birth_date': '1989-08-23',
        'initial_assets': (6000, 8000),
        'salary': (3000, 3500),
        'has_partner': True,
        'partner_works': True,
        'children': 0,
        'owns_house': True,
        'has_car': True,
        'index_fix_expenses': 1,
        'index_var_expenses': 0.5,
    },
    'buyer_4': {
        'name': 'Jorge',
        'surname': 'Moreno',
        'city': 'Galdakao',
        'birth_date': '1974-05-23',
        'initial_assets': (5000, 6000),
        'salary': (1000, 3000),
        'has_partner': True,
        'partner_works': False,
        'children': 3,
        'owns_house': True,
        'has_car': True,
        'index_fix_expenses': 1,
        'index_var_expenses': 1.1,
    },
    'buyer_5': {
        'name': 'Sara',
        'surname': 'Gurrutxaga',
        'city': 'Donostia',
        'birth_date': '1994-03-12',
        'initial_assets': (1000, 2000),
        'salary': (2100, 2800),
        'has_partner': True,
        'partner_works': True,
        'children': 0,
        'owns_house': True,
        'has_car': False,
        'index_fix_expenses': 1,
        'index_var_expenses': 0.5,
    },
    'buyer_6': {
        'name': 'Manuel',
        'surname': 'Rodríguez',
        'city': 'Vitoria-Gasteiz',
        'birth_date': '1979-02-14',
        'initial_assets': (1000, 2000),
        'salary': (1100, 3000),
        'has_partner': False,
        'partner_works': False,
        'children': 0,
        'owns_house': True,
        'has_car': False,
        'index_fix_expenses': 1,
        'index_var_expenses': 1.5,
    },
    'buyer_7': {
        'name': 'María',
        'surname': 'Valdec',
        'city': 'Portugalete',
        'birth_date': '1968-12-31',
        'initial_assets': (10000, 1500),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': False,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'index_fix_expenses': 1,
        'index_var_expenses': 0.7,
    },
    'buyer_8': {
        'name': 'Antonio',
        'surname': 'Miranda',
        'city': 'Labastida',
        'birth_date': '1979-04-04',
        'initial_assets': (1000, 2000),
        'salary': (2000, 4000),
        'has_partner': False,
        'partner_works': False,
        'children': 0,
        'owns_house': True,
        'has_car': True,
        'index_fix_expenses': 1.1,
        'index_var_expenses': 1.2,
    }
}


# Generate IBAN for each profile
for profile in buyer_profiles.values():
    bank_code = "2095"
    branch_code = f"{random.randint(0, 9999):04d}"
    account_number = f"{random.randint(0, 9999999999):010d}"
    control_digits = calculate_iban_control_digits(bank_code, branch_code, account_number)
    profile['iban'] = f"ES{control_digits}{bank_code}{branch_code}{account_number}"


# Generate DNI for each profile
for profile in buyer_profiles.values():
    profile['dni'] = generate_spanish_dni()


# Generate password for each profile
for profile in buyer_profiles.values():
    profile['password'] = generate_password(6)


consumption_profile = {
    "annual" : [
        {"concept": "taxes", "range": (1200, 1800)},
        {"concept": "insurance", "range": (300, 600)}
    ],
    "monthly" : {
        "basic_services": [
            {"concept": "water", "range": (20, 45)},
            {"concept": "electricity", "range": (20, 90)},
            {"concept": "gas", "range": (30, 115)},
            {"concept": "internet", "range": (42, 42)},
            {"concept": "phone", "range": (30, 45)}
        ],
        "housing": [
            {"concept": "rent", "range": (600, 800)},
            {"concept": "mortgage", "range": (700, 1100)},
        ]
    },
    "frequent": [
        {"concept": "food", "range": (60, 125), "frequency": 0.15},
        {"concept": "transport", "range": (40, 90), "frequency": 0.1},
        {"concept": "leisure", "range": (18, 85), "frequency": 0.12},
        {"concept": "clothing", "range": (45, 160), "frequency": 0.05},
        {"concept": "healthcare", "range": (38, 190), "frequency": 0.03},
        {"concept": "education", "range": (42, 79), "frequency": 0.04},
        {"concept": "cash", "range": (100, 100), "frequency": 0.17},

    ],
    "occasional": [
        {"concept": "travel", "range": (280, 1900), "frequency": 0.015},
        {"concept": "appliances", "range": (75, 420), "frequency": 0.03},
        {"concept": "repairs", "range": (27, 333), "frequency": 0.07},
        {"concept": "gifts", "range": (25, 850), "frequency": 0.06}
    ],
    "conditional": [
        {"concept": "children", "range": (50, 280), "frequency": 0.04},
        {"concept": "car", "range": (120, 330), "frequency": 0.004},
    ]
}
