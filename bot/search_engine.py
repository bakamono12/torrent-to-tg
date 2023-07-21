import json
import os
import re
import string
import requests
import random
import time
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import jsbeautifier

# keep track of latest url
latest_url_file = "latest_urls.jsonl"


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
    if os.path.exists(latest_url_file):
        with open(latest_url_file, 'r') as f:
            latest_url = f.read()
        last_url = json.loads(latest_url)[-1]
        if last_url:
            url = last_url['url']
            if url:
                random_str = generate_random_string(8)
                url += "/" + title + f"/{random_str}/0/SEED/NONE/1?_={time.time()}"
                results = get_movie_results(url)
                if results:
                    return results
                else:
                    results = new_url(title)
                    return results
            else:
                return None
    else:
        results = new_url(title)
        return results


def new_url(title):
    # Generate latest URL
    ua = UserAgent().random
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
    pattern = r'var\s+(\w+)\s*=\s*"([^"]+)";'
    pretty_js = jsbeautifier.beautify_file('script.js')

    matches = re.findall(pattern, pretty_js)
    for var_name, var_value in matches:
        if len(var_name) > 1:
            os.remove('script.js')
            save_url(page_url + "/" + var_value)
            url = page_url + "/" + var_value + "/" + title + f"/{part2}/0/SEED/NONE/1?_={current_time}"
            return get_movie_results(url)
        else:
            continue


def save_url(url):
    # save the latest url in file
    if os.path.exists(latest_url_file):
        with open(latest_url_file, 'r') as f:
            latest_url = f.read()
        latest_url = json.loads(latest_url)
        latest_url.append({"url": url})
        with open(latest_url_file, 'w') as f:
            f.write(json.dumps(latest_url))
    else:
        with open(latest_url_file, 'w') as f:
            f.write(json.dumps([{"url": url}]))


data = generate_url("Men%20in%20Black")
print(data)
