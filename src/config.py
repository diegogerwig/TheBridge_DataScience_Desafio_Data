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
        'salary': (1001, 1500),
        'initial_balance_range': (100, 1000),
        'trx_range': (10, 500),
        'trx_weights': [0.4, 0.4, 0.2],
        'trx_frequency': 3,
        'children': 0,
        'owns_house': False,
        'has_car': False,
        'has_partner': False,
        'partner_works': False
    },
    'buyer_2': {
        'name': 'Carmen',
        'city': 'Zarautz',
        'age': 40,
        'salary': (1501, 2000),
        'initial_balance_range': (500, 2000),
        'trx_range': (20, 800),
        'trx_weights': [0.35, 0.35, 0.3],
        'trx_frequency': 4,
        'children': 1,
        'owns_house': False,
        'has_car': True,
        'has_partner': True,
        'partner_works': False
    },
    'buyer_3': {
        'name': 'Ana',
        'city': 'Amurrio',
        'age': 35,
        'salary': (2001, 2500),
        'initial_balance_range': (1000, 5000),
        'trx_range': (50, 1000),
        'trx_weights': [0.3, 0.3, 0.4],
        'trx_frequency': 5,
        'children': 1,
        'owns_house': False,
        'has_car': True,
        'has_partner': True,
        'partner_works': True
    },
    'buyer_4': {
        'name': 'Jorge',
        'city': 'Galdakao',
        'age': 50,
        'salary': (2501, 3000),
        'initial_balance_range': (2000, 10000),
        'trx_range': (100, 1500),
        'trx_weights': [0.25, 0.25, 0.5],
        'trx_frequency': 6,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_partner': True,
        'partner_works': True
    },
    'buyer_5': {
        'name': 'Sara',
        'city': 'Donostia',
        'age': 30,
        'salary': (3001, 4000),
        'initial_balance_range': (5000, 20000),
        'trx_range': (100, 2000),
        'trx_weights': [0.2, 0.3, 0.5],
        'trx_frequency': 7,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_partner': True,
        'partner_works': True
    },
    'buyer_6': {
        'name': 'Manuel',
        'city': 'Vitoria-Gasteiz',
        'age': 45,
        'salary': (1200, 1800),
        'initial_balance_range': (200, 1500),
        'trx_range': (15, 600),
        'trx_weights': [0.45, 0.35, 0.2],
        'trx_frequency': 4,
        'children': 0,
        'owns_house': False,
        'has_car': False,
        'has_partner': False,
        'partner_works': False
    },
    'buyer_7': {
        'name': 'María',
        'city': 'Portugalete',
        'age': 56,
        'salary': (2800, 3500),
        'initial_balance_range': (3000, 15000),
        'trx_range': (80, 1800),
        'trx_weights': [0.2, 0.3, 0.5],
        'trx_frequency': 6,
        'children': 3,
        'owns_house': True,
        'has_car': True,
        'has_partner': True,
        'partner_works': True
    },
    'buyer_8': {
        'name': 'Antonio',
        'city': 'Labastida',
        'age': 45,
        'salary': (1800, 2300),
        'initial_balance_range': (800, 3000),
        'trx_range': (30, 900),
        'trx_weights': [0.3, 0.4, 0.3],
        'trx_frequency': 5,
        'children': 1,
        'owns_house': True,
        'has_car': True,
        'has_partner': True,
        'partner_works': False
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
        {"concept": "taxes", "range": (200, 5000)},
        {"concept": "insurance", "range": (100, 2000)}
    ],
    "monthly" : {
        "basic_services": [
            {"concept": "water", "range": (10, 80)},
            {"concept": "electricity", "range": (20, 150)},
            {"concept": "gas", "range": (15, 100)},
            {"concept": "internet", "range": (30, 80)},
            {"concept": "phone", "range": (20, 100)}
        ],
        "housing": [
            {"concept": "rent", "range": (300, 1500)},
            {"concept": "mortgage", "range": (400, 2000)},
            # {"concept": "maintenance", "range": (50, 300)}
        ]
    },
    "frequent": [
        {"concept": "food", "range": (100, 800), "frequency": 0.9},
        {"concept": "transport", "range": (20, 200), "frequency": 0.8},
        {"concept": "leisure", "range": (10, 300), "frequency": 0.6},
        {"concept": "clothing", "range": (30, 500), "frequency": 0.4},
        {"concept": "healthcare", "range": (20, 400), "frequency": 0.3},
        {"concept": "education", "range": (50, 1000), "frequency": 0.2}
    ],
    "occasional": [
        {"concept": "travel", "range": (200, 3000), "frequency": 0.1},
        {"concept": "appliances", "range": (100, 2000), "frequency": 0.05},
        {"concept": "repairs", "range": (50, 1000), "frequency": 0.15},
        {"concept": "gifts", "range": (20, 500), "frequency": 0.2}
    ],
    "conditional": [
        {"concept": "children", "range": (50, 500), "frequency": 0.5, "multiplier": 1.5},
        {"concept": "car", "range": (30, 300), "frequency": 0.4},
    ]
}

trx_cat = [
    'food',
    'housing',
    'transport',
    'basic-services',
    'leisure',
    'healthcare',
    'education',
    'clothing',
    'technology',
    'savings',
    'loans',
    'personal_care',
    'subscriptions',
    'children_exp',
    'car_exp'
]