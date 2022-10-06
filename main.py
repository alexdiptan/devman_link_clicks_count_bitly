import os
import argparse

from dotenv import load_dotenv
from urllib.parse import urlparse
import requests


def shorten_link(user_input, token: str) -> str:
    url = 'https://api-ssl.bitly.com/v4/shorten'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {'long_url': user_input}

    bitlink = requests.post(url, json=payload, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['link']


def count_clicks(token: str, link: str) -> str:
    link_parts = urlparse(link)
    link = ''.join([link_parts.netloc, link_parts.path])
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'
    bitlink = requests.get(url, headers=headers)
    bitlink.raise_for_status()

    return bitlink.json()['total_clicks']


def is_bitlink(token: str, bitlink: str) -> bool:
    link_parts = urlparse(bitlink)
    bitlink = ''.join([link_parts.netloc, link_parts.path])
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    response = requests.get(url, headers=headers)

    return response.ok


def main():
    load_dotenv()
    bitly_token = os.environ['BITLY_TOKEN']

    if is_bitlink(bitly_token, args.user_link):
        try:
            print(f'Кол-во переходов по ссылке битли: {count_clicks(bitly_token, args.user_link)}')
        except requests.exceptions.HTTPError:
            print('Не удалось получить кол-во кликов')
    else:
        try:
            print(f'Битлинк {shorten_link(args.user_link, bitly_token)}')
        except requests.exceptions.HTTPError:
            print('Вы ввели не корректную ссылку')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт создает битли-ссылку')
    parser.add_argument('user_link', help='Ссылка')
    args = parser.parse_args()

    main()
