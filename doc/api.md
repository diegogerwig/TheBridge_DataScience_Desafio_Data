https://dashboard.render.com/

https://thebridge-datascience-desafio-data.onrender.com/docs
https://thebridge-datascience-desafio-data.onrender.com/users
https://thebridge-datascience-desafio-data.onrender.com/transactions?from_date=2024-10-03


# Ejemplo de petición usando CURL en la terminal

curl -X GET "https://thebridge-datascience-desafio-data.onrender.com/users"


# Ejemplo de petición usando Python requests

import requests

#Para todos los perfiles
url = "https://thebridge-datascience-desafio-data.onrender.com/transactions"
params = {
    "from_date": "2022-01-01"
}
response = requests.get(url, params=params)
print(response.json())

#Para un perfil específico
params = {
    "from_date": "2022-01-01",
    "profile": "buyer_1"
}
response = requests.get(url, params=params)
print(response.json())


# Ejemplo de petición usando JavaScript fetch

// Para todos los perfiles
fetch('https://thebridge-datascience-desafio-data.onrender.com/transactions?from_date=2022-01-01')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// Para un perfil específico
fetch('https://thebridge-datascience-desafio-data.onrender.com/transactions?from_date=2022-01-01&profile=buyer_1')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));



# Explicación del Endpoint de la API

Base URL: https://thebridge-datascience-desafio-data.onrender.com
Endpoint: /transactions
Método HTTP: GET
Parámetros de consulta:
  - from_date (obligatorio): La fecha de inicio para generar transacciones (formato: YYYY-MM-DD)
  - profile (opcional): El perfil específico para el cual generar transacciones

Ejemplo de URL completa con parámetros:
https://thebridge-datascience-desafio-data.onrender.com/transactions?from_date=2022-01-01&profile=buyer_1

Este endpoint permite:
1. Generar transacciones para todos los perfiles si no se especifica un perfil.
2. Generar transacciones para un perfil específico si se proporciona el parámetro 'profile'.