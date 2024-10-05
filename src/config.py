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

perfil_consumos = [
    {
        "anual" : [
            "impuestos",
            "seguros"
        ],
        "mensual" : {
            "agua" : (10, 30),
            "luz" : (10, 50),
            "comunicación" : (30, 80)
        },
        "otros": [
            "gasolina"
        ]

    }
]

categorias_trx = [
    'Alimentación',
    'Entretenimiento',
    'Básicos', 
    'Ocio',
    'Transporte'
]
