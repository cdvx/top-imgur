import logging
import os
from functools import partial
from multiprocessing import Pool
from time import time

from download import setup_download_dir, get_links, download_link
from config import Config

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


def main():

    ts = time()
    client_id = Config.CLIENT_ID
    if not client_id:
        raise Exception("Please add IMGUR `CLIENT_ID` environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    download = partial(download_link, download_dir)

    with Pool(4) as p:
        p.map(download, links)
    logging.info(f'Prcoess Took: {time() - ts} seconds')
    logging.info(f'Size of images directory: {os.path.getsize(download_dir)}')
    logging.info(f'Number of images downloaded: {len(os.listdir(download_dir))}')

if __name__ == '__main__':
    main()