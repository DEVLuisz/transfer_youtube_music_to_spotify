import requests
import json

# Substitua pelos seus cookies válidos
cookies = {
    "SAPISID": "SEU SAPISID",
    "APISID": "SEU APISID",
    "HSID": "SEU HSID",
    "SID": "SEU SID",
    "SIDCC": "SEU SIDCC"
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "Content-Type": "application/json"
}

data = {
    "context": {
        "client": {
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20240101.01.00"
        }
    }
}

response = requests.post("https://music.youtube.com/youtubei/v1/browse", headers=headers, cookies=cookies, data=json.dumps(data))

if response.status_code == 200:
    print("Autenticação bem-sucedida! ✅")
    print("Resposta da API:", response.json())  # Exibe a resposta JSON da API
else:
    print(f"Erro {response.status_code}: {response.text}")
