from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from past.utils import old_div
import sys
from .progressbar import *
from .utils import ImageScraper, download_worker_fn
from .exceptions import *
from setproctitle import setproctitle
import SimplePool
import threading


def console_main():
    setproctitle('image-scraper')
    scraper = ImageScraper()
    scraper.get_arguments()
    print("\nImageScraper\n============\nRequesting page....\n")
    try:
        scraper.get_html()
    except PageLoadError as e:
        scraper.page_html = ""
        scraper.page_url = ""
        print("Page failed to load. Status code: {0}".format(e.status_code))
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

    status_flags = {'count': 0, 'percent': 0.0, 'failed': 0, 'over_max_filesize': 0}
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=100).start()
    pool = SimplePool.ThreadPool()
    status_lock = threading.Lock()
    for img_url in scraper.images:
        if status_flags['count'] == scraper.no_to_download:
            break
        download_job = SimplePool.ThreadJob(download_worker_fn, (scraper, img_url, pbar, status_flags, status_lock))
        pool.add_job(download_job)
        status_flags['count'] += 1

    pool.start()
    pool.finish()

    pbar.finish()
    print("\nDone!\nDownloaded {0} images\nFailed: {1}\n".format(
          status_flags['count']-status_flags['failed']-status_flags['over_max_filesize'], status_flags['failed']))
    return


def scrape_images(url, no_to_download=None,
                  format_list=["jpg", "png", "gif", "svg", "jpeg"],
                  download_path='images', max_filesize=100000000,
                  dump_urls=False, use_ghost=False):
    #  Broken due to wrapping in class. Need to fix!
    page_html, page_url = get_html(url, use_ghost)
    images = get_img_list(page_html, page_url, format_list)

    download_path = os.path.join(os.getcwd(), download_path)

    if len(images) == 0:
        return 0, 0  # count, failed
    if no_to_download is None:
        no_to_download = len(images)

    process_download_path(download_path)

    count = 0
    failed = 0
    over_max_filesize = 0

    for img_url in images:
        if count == no_to_download:
            break
        try:
            download_image(img_url, download_path, max_filesize)
        except ImageDownloadError:
            failed += 1
        except ImageSizeError:
            over_max_filesize += 1
        count += 1
    return count, failed
