"""
Configurations for our transaction generation system    
"""

income_profiles = {
    # 'Low income': 
    # {
    #     'salary' : (500, 1500),
    #     'initial_balance_range': (100, 1000),
    #     'transaction_range': (10, 500),
    #     'transaction_weights': [0.4, 0.4, 0.2],
    #     'transaction_frequency': 3,
    #     'children': 0,
    #     'owns_house': False,
    #     'has_car': False,
    #     'has_pet': False,
    #     'has_partner': False,
    #     'partner_works': False
    # },
    # 'Average income' : 
    # {
    #     'salary' : (1000, 2000),
    #     'initial_balance_range': (1000, 10000),
    #     'transaction_range': (50, 2000),
    #     'transaction_weights': [0.3, 0.3, 0.4],
    #     'transaction_frequency': 5,
    #     'children': 1,
    #     'owns_house': False,
    #     'has_car': True,
    #     'has_pet': True,
    #     'has_partner': True,
    #     'partner_works': True
    # },
    # 'High income': 
    # {
    #     'salary' : (2500, 4000),
    #     'initial_balance_range': (10000, 100000),
    #     'transaction_range': (100, 10000),
    #     'transaction_weights': [0.2, 0.2, 0.6],
    #     'transaction_frequency': 7,
    #     'children': 2,
    #     'owns_house': True,
    #     'has_car': True,
    #     'has_pet': True,
    #     'has_partner': True,
    #     'partner_works': True
    # },
    'Very Low income': {
        'salary': (0, 1000),
        'initial_balance_range': (0, 500),
        'transaction_range': (5, 200),
        'transaction_weights': [0.5, 0.3, 0.2],
        'transaction_frequency': 2,
        'children': 0,
        'owns_house': False,
        'has_car': False,
        'has_pet': False,
        'has_partner': False,
        'partner_works': False
    },
    'Low income': {
        'salary': (1001, 1500),
        'initial_balance_range': (100, 1000),
        'transaction_range': (10, 500),
        'transaction_weights': [0.4, 0.4, 0.2],
        'transaction_frequency': 3,
        'children': 0,
        'owns_house': False,
        'has_car': False,
        'has_pet': False,
        'has_partner': False,
        'partner_works': False
    },
    'Lower Middle income': {
        'salary': (1501, 2000),
        'initial_balance_range': (500, 2000),
        'transaction_range': (20, 800),
        'transaction_weights': [0.35, 0.35, 0.3],
        'transaction_frequency': 4,
        'children': 1,
        'owns_house': False,
        'has_car': True,
        'has_pet': False,
        'has_partner': True,
        'partner_works': False
    },
    'Middle income': {
        'salary': (2001, 2500),
        'initial_balance_range': (1000, 5000),
        'transaction_range': (50, 1000),
        'transaction_weights': [0.3, 0.3, 0.4],
        'transaction_frequency': 5,
        'children': 1,
        'owns_house': False,
        'has_car': True,
        'has_pet': True,
        'has_partner': True,
        'partner_works': True
    },
    'Upper Middle income': {
        'salary': (2501, 3000),
        'initial_balance_range': (2000, 10000),
        'transaction_range': (100, 1500),
        'transaction_weights': [0.25, 0.25, 0.5],
        'transaction_frequency': 6,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_pet': True,
        'has_partner': True,
        'partner_works': True
    },
    'Lower High income': {
        'salary': (3001, 4000),
        'initial_balance_range': (5000, 20000),
        'transaction_range': (100, 2000),
        'transaction_weights': [0.2, 0.3, 0.5],
        'transaction_frequency': 7,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_pet': True,
        'has_partner': True,
        'partner_works': True
    },
    'High income': {
        'salary': (4001, 6000),
        'initial_balance_range': (10000, 50000),
        'transaction_range': (100, 5000),
        'transaction_weights': [0.2, 0.2, 0.6],
        'transaction_frequency': 8,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_pet': True,
        'has_partner': True,
        'partner_works': True
    },
    'Very High income': {
        'salary': (6001, 10000),
        'initial_balance_range': (20000, 100000),
        'transaction_range': (200, 10000),
        'transaction_weights': [0.1, 0.2, 0.7],
        'transaction_frequency': 10,
        'children': 2,
        'owns_house': True,
        'has_car': True,
        'has_pet': True,
        'has_partner': True,
        'partner_works': True
    }
}


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
            {"concept": "maintenance", "range": (50, 300)}
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
        {"concept": "pet", "range": (20, 200), "frequency": 0.3}
    ]
}

transaction_categories = [
    'Food',
    'Housing',
    'Transport',
    'Basic services',
    'Leisure and entertainment',
    'Healthcare',
    'Education',
    'Clothing and accessories',
    'Technology',
    'Savings and investment',
    'Debts and loans',
    'Donations and charity',
    'Pets',
    'Personal care',
    'Subscriptions',
    'Minor expenses',
    'Children expenses',
    'Car expenses'
]

# List of municipalities in the Basque Country
cities = [
    # Bizkaia
    "Bilbao", "Barakaldo", "Getxo", "Portugalete", "Santurtzi", "Basauri", "Leioa", 
    "Galdakao", "Sestao", "Durango", "Erandio", "Bermeo", "Mungia", "Sopela", "Berango",
    # Gipuzkoa
    "San Sebastian", "Irun", "Errenteria", "Eibar", "Zarautz", "Arrasate/Mondragon", 
    "Hernani", "Lasarte-Oria", "Hondarribia", "Pasaia", "Andoain",
    # Araba
    "Vitoria-Gasteiz", "Llodio", "Amurrio", "Salvatierra/Agurain", "Oyón-Oion", 
    "Iruña de Oca", "Alegría-Dulantzi", "Zuia", "Labastida/Bastida", "Elciego"
]