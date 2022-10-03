from dotenv import load_dotenv
import requests
import os


def shorten_link(user_input, token: str) -> str:
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': user_input}

    bitlink = requests.post(url, json=payload, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['link']


def count_clicks(token: str, link: str) -> str:
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    bitlink = requests.get(url, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['total_clicks']


def is_bitlink(token: str, bitlink: str) -> bool:
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)

    return response.ok


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']
    user_input = input('Введите ссылку: ')

    if is_bitlink(bitly_token, user_input):
        try:
            print(f'Кол-во кликов: {count_clicks(bitly_token, user_input)}')
        except requests.exceptions.HTTPError:
            print('Не удалось получить кол-во кликов')
    else:
        try:
            print(f'Битлинк {shorten_link(user_input, bitly_token)}')
        except requests.exceptions.HTTPError:
            print('Вы ввели не корректную ссылку')


if __name__ == '__main__':
    main()
