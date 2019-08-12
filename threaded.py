import logging
import os
from queue import Queue
from threading import Thread
from time import time

from download import setup_download_dir, get_links, download_link
from config import Config


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


class ImageDownloadWorker(Thread):
    """Worker class for image download tasks"""

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        # run infitnite loop
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
                download_link(directory, link)
            finally:
                self.queue.task_done()


def main():
    ts = time()
    client_id = Config.CLIENT_ID
    if not client_id:
        raise Exception("Please add IMGUR `CLIENT_ID` environment variable!")
    download_dir = setup_download_dir()
    links = get_links(client_id)
    # Create a queue to communicate with the worker threads
    queue = Queue()

    # Create 8 worker threads
    for x in range(8):
        worker = ImageDownloadWorker(queue)

        # Setting daemon to True will let the main 
        # thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in links:
        logger.info('Queueing {}'.format(link))
        queue.put((download_dir, link))
    
    # Causes the main thread to wait for the queue
    # to finish processing all the tasks
    queue.join()
    logging.info(f'Prcoess Took: {time() - ts} seconds')
    logging.info(f'Size of images directory: {os.path.getsize(download_dir)}')
    logging.info(f'Number of images downloaded: {len(os.listdir(download_dir))}')

if __name__ == '__main__':
    main()