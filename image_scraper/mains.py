""" Main file containing console command code. """

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from .progressbar import ProgressBar, Percentage, Bar, RotatingMarker, ETA, FileTransferSpeed
from .utils import ImageScraper, download_worker_fn
from .exceptions import DirectoryAccessError, DirectoryCreateError, PageLoadError
from setproctitle import setproctitle
from concurrent.futures import ThreadPoolExecutor
import threading
import sys


def main():
    """ Called when the command is executed

        Calls the function that starts the script
        handles KeyboardInterrupt
    """
    try:
        console_main()
    except KeyboardInterrupt:
        print ("Scraping stopped by user.")

def console_main():
    """ This function handles all the console action. """
    setproctitle('image-scraper')
    scraper = ImageScraper()
    scraper.get_arguments()
    print("\nImageScraper\n============\nRequesting page....\n")
    try:
        scraper.get_html()
    except PageLoadError as err:
        if err.status_code is None:
            print("ImageScraper is unable to acces the internet.")
        else:
            print("Page failed to load. Status code: {0}".format(err.status_code))
        sys.exit()

    scraper.get_img_list()

    if len(scraper.images) == 0:
        sys.exit("Sorry, no images found.")
    if scraper.no_to_download is None:
        scraper.no_to_download = len(scraper.images)

    print("Found {0} images: ".format(len(scraper.images)))

    try:
        scraper.process_download_path()
    except DirectoryAccessError:
        print("Sorry, the directory can't be accessed.")
        sys.exit()
    except DirectoryCreateError:
        print("Sorry, the directory can't be created.")
        sys.exit()

    if scraper.dump_urls:
        for img_url in scraper.images:
            print(img_url)

    status_flags = {'count': 0, 'percent': 0.0, 'failed': 0, 'under_min_or_over_max_filesize': 0}
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=100).start()
    pool = ThreadPoolExecutor(max_workers=scraper.nthreads)
    status_lock = threading.Lock()
    for img_url in scraper.images:
        if status_flags['count'] == scraper.no_to_download:
            break
        pool.submit(download_worker_fn, scraper, img_url, pbar, status_flags, status_lock)
        status_flags['count'] += 1
    pool.shutdown(wait=True)
    pbar.finish()
    print("\nDone!\nDownloaded {0} images\nFailed: {1}\n".format(
        status_flags['count']-status_flags['failed']-status_flags['under_min_or_over_max_filesize'],
        status_flags['failed']))
    return

