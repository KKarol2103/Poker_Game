import requests


def get_request_from_server():
    params = {"hole": 'Ac,3c'}
    headers = {
        'X-RapidAPI-Key': '27d78d9697msh53ab6c2d6d05fa0p182b9ejsnccf4cb1e9b8c',
        'X-RapidAPI-Host': 'sf-api-on-demand-poker-odds-v1.p.rapidapi.com'
    }
    response = requests.get("https://sf-api-on-demand-poker-odds-v1.p.rapidapi.com/pre-flop", headers=headers, params=params)
    print(response.text)


get_request_from_server()