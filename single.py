import logging
import os
from time import time

from download import setup_download_dir, get_links, download_link
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    ts = time()
    client_id = Config.CLIENT_ID
    if not client_id:
        raise Exception("Please add IMGUR `CLIENT_ID` environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    for link in links:
        download_link(download_dir, link)
    logging.info(f'Prcoess Took: {time() - ts} seconds')
    logging.info(f'Size of images directory: {os.path.getsize(download_dir)}')
    logging.info(f'Number of images downloaded: {len(os.listdir(download_dir))}')

if __name__ == '__main__':
    main()