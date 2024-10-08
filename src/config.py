import random
from utils import calculate_iban_control_digits

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
    'buyer_1': {
        'name': 'Luis',
        'city': 'Bilbao',
        'age': 28,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_2': {
        'name': 'Carmen',
        'city': 'Zarautz',
        'age': 40,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_3': {
        'name': 'Ana',
        'city': 'Amurrio',
        'age': 35,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_4': {
        'name': 'Jorge',
        'city': 'Galdakao',
        'age': 50,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_5': {
        'name': 'Sara',
        'city': 'Donostia',
        'age': 30,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_6': {
        'name': 'Manuel',
        'city': 'Vitoria-Gasteiz',
        'age': 45,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_7': {
        'name': 'María',
        'city': 'Portugalete',
        'age': 56,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    },
    'buyer_8': {
        'name': 'Antonio',
        'city': 'Labastida',
        'age': 45,
        'initial_balance_range': (1000, 2000),
        'salary': (1200, 1500),
        'has_partner': True,
        'partner_works': True,
        'children': 1,
        'owns_house': True,
        'has_car': False,
    }
}


# Generate IBAN for each profile
for profile in buyer_profiles.values():
    bank_code = "2095"
    branch_code = f"{random.randint(0, 9999):04d}"
    account_number = f"{random.randint(0, 9999999999):010d}"
    control_digits = calculate_iban_control_digits(bank_code, branch_code, account_number)
    profile['iban'] = f"ES{control_digits}{bank_code}{branch_code}{account_number}"


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
