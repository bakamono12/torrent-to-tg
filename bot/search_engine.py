import os
import re
import string
import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import jsbeautifier


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def get_movie_results(url):
    ua = UserAgent().random

    headers = {
        'authority': 'snowfl.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': 'laf=fa1',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://snowfl.com',
        'user-agent': ua,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None
    data = response.json()
    return data


def generate_url(title):
    ua = UserAgent().random
    # Generate timestamp for URL
    current_time = int(time.time())
    part2 = generate_random_string(8)
    headers = {
        'authority': 'snowfl.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': 'laf=fa1',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://snowfl.com',
        'user-agent': ua,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }
    page_url = "https://snowfl.com"
    get_page = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(get_page.content, 'html.parser')
    # pick the javascript src
    script = soup.find_all('script')[2]
    # get the src
    src = page_url + "/" + script['src']
    # visit the src
    get_page = requests.get(src)
    with open('script.js', 'w') as f:
        f.write(get_page.text)
    # url: "/" + bPMSrddX + "/newsfeed", capture the variable name
    pattern = r'var\s+(\w+)\s*=\s*"([^"]+)";'
    pretty_js = jsbeautifier.beautify_file('script.js')

    # Step 4: Search for the dynamic variable assignment in the JavaScript code
    matches = re.findall(pattern, pretty_js)
    for var_name, var_value in matches:
        if len(var_name) > 1:
            os.remove('script.js')
            url = page_url + "/" + var_value + "/" + title + f"/{part2}/0/NONE/NONE/1?_={current_time}"
            return get_movie_results(url)
        else:
            continue


# generate_url("The%20Matrix")