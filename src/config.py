"""
Configuraciones de nuestro sistema de generación de transacciones    
"""

perfiles_ingreso = {
    'Bajos ingresos': 
    {
        'nomina' : (500, 1500),
        'initial_balance_range': (100, 1000),
        'transaction_range': (10, 500),
        'transaction_weights': [0.4, 0.4, 0.2],
        'transaction_frequency': 3
    },
    'Ingresos promedio' : 
    {
        'nomina' : (1000, 2000),
        'initial_balance_range': (1000, 10000),
        'transaction_range': (50, 2000),
        'transaction_weights': [0.3, 0.3, 0.4],
        'transaction_frequency': 5
    },
    'Altos ingresos': 
    {
        'nomina' : (2500, 4000),
        'initial_balance_range': (10000, 100000),
        'transaction_range': (100, 10000),
        'transaction_weights': [0.2, 0.2, 0.6],
        'transaction_frequency': 7
    }
}

perfil_consumos = {
    "anual" : [
        {"concepto": "impuestos", "rango": (200, 5000)},
        {"concepto": "seguros", "rango": (100, 2000)}
    ],
    "mensual" : {
        "servicios_basicos": [
            {"concepto": "agua", "rango": (10, 80)},
            {"concepto": "luz", "rango": (20, 150)},
            {"concepto": "gas", "rango": (15, 100)},
            {"concepto": "internet", "rango": (30, 80)},
            {"concepto": "telefonía", "rango": (20, 100)}
        ],
        "vivienda": [
            {"concepto": "alquiler", "rango": (300, 1500)},
            {"concepto": "hipoteca", "rango": (400, 2000)},
            {"concepto": "mantenimiento", "rango": (50, 300)}
        ]
    },
    "frecuentes": [
        {"concepto": "alimentación", "rango": (100, 800), "frecuencia": 0.9},
        {"concepto": "transporte", "rango": (20, 200), "frecuencia": 0.8},
        {"concepto": "ocio", "rango": (10, 300), "frecuencia": 0.6},
        {"concepto": "ropa", "rango": (30, 500), "frecuencia": 0.4},
        {"concepto": "salud", "rango": (20, 400), "frecuencia": 0.3},
        {"concepto": "educación", "rango": (50, 1000), "frecuencia": 0.2}
    ],
    "ocasionales": [
        {"concepto": "viajes", "rango": (200, 3000), "frecuencia": 0.1},
        {"concepto": "electrodomésticos", "rango": (100, 2000), "frecuencia": 0.05},
        {"concepto": "reparaciones", "rango": (50, 1000), "frecuencia": 0.15},
        {"concepto": "regalos", "rango": (20, 500), "frecuencia": 0.2}
    ]
}

categorias_trx = [
    'Alimentación',
    'Vivienda',
    'Transporte',
    'Servicios básicos',
    'Ocio y entretenimiento',
    'Salud',
    'Educación',
    'Ropa y accesorios',
    'Tecnología',
    'Ahorro e inversión',
    'Deudas y préstamos',
    'Donaciones y caridad',
    'Mascotas',
    'Cuidado personal',
    'Subscripciones'
]