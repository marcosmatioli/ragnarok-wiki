import requests
import json
import time

lista_monstro = []
tempo = 1 # tempo em segundos

for n in range(3976 , 5000):
    time.sleep(tempo) # delay de 1 segundo
    # URL da API que você deseja acessar
    #url = f"https://www.divine-pride.net/api/database/Monster/{n}?apiKey=b046df176ec0964286fc4b5ba8b3c84a" # marcos
    url = f"https://www.divine-pride.net/api/database/Monster/{n}?apiKey=d8a0fbd9a7f4dfd9d330170bcfb2bfee" # rafael
    cabecalhos = {'Accept-Language': 'pt-BR'}

    # Envia uma solicitação GET
    response = requests.get(url, headers=cabecalhos)

    # Verifica o status da resposta
    if response.status_code == 200:  # 200 significa sucesso
        data = response.json()  # Converte a resposta JSON em um dicionário ou lista
        if data['name'] not in ('', None, 'null'):
            filtrojson = {"id": data["id"],"name":data["name"]} #isso filtro o json acima
            lista_monstro.append(filtrojson)
            print(filtrojson)

            json_list = json.dumps(lista_monstro)
            with open('templates/data.json', "w") as arquivo:
                arquivo.write(json_list)
                arquivo.close()
    else:
        print(f'Erro na requisição. Código de status: {response.status_code}')

