import json
import logging
import os
from pathlib import Path
import requests
from urllib.request import urlopen

logger = logging.getLogger(__name__)

types = {'image/jpeg', 'image/png'}

def get_links(client_id):
    # fetch a list of images
    header = {
                'Authorization': f'Client-ID {client_id}',
                'Accept': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    req = requests.get(make_url('random', 'random'), headers=header)

    data = req.json()['data']
    return [item['link'] for item in data if 'type' in item and item['type'] in types]


def download_link(directory, link):
    # download and save images
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.read())
    logger.info(f'Downloaded {link}')

def make_url(r1, r2):
    # format url with args passed
    return f'https://api.imgur.com/3/gallery/{r1}/{r2}/'


def setup_download_dir():
    # create download directory if 
    # it doesn't exist
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir