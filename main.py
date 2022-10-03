from dotenv import load_dotenv
import requests
import os

load_dotenv()


def shorten_link(url_to_create, token: str) -> str:
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': f'{url_to_create}'}

    bitlink = requests.post(url, json=payload, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['link']


def count_clicks(token: str, link: str) -> str:
    headers = {'Authorization': f'Bearer {token}'}
    params = {'unit': 'day', 'units': '-1'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    bitlink = requests.get(url, params=params, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['total_clicks']


def is_bitlink(token: str, bitlink: str) -> bool:
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)

    return response.ok


def main():
    my_token = os.environ['TOKEN']
    link_to_process = input('Введите ссылку: ')  # https://encyclopedia2.thefreedictionary.com

    if is_bitlink(my_token, link_to_process):
        try:
            print(f'Кол-во кликов: {count_clicks(my_token, link_to_process)}')
        except requests.exceptions.HTTPError:
            print('Не удалось получить кол-во кликов')
    else:
        try:
            print(f'Битлинк {shorten_link(link_to_process, my_token)}')
        except requests.exceptions.HTTPError:
            print('Вы ввели не корректную ссылку')


if __name__ == '__main__':
    main()
