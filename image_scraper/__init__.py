
import sys
from lxml import html
import requests
import urlparse
import os
from progressbar import *
import argparse
from utils import process_links, get_html, get_img_list, download_image, process_download_path, get_arguments

def console_main():
    URL, no_to_download, download_path, use_ghost = get_arguments()

    print "\n ImageScraper\n ============\n Requesting page....\n"

    page_html, page_url = get_html(URL, use_ghost)
    images = get_img_list(page_html, page_url)

    if len(images) == 0:
        sys.exit("Sorry, no images found.")
    print "Found %s images: " % len(images)

    process_download_path(download_path)

    count = 0
    percent = 0.0
    failed = 0
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=100).start()

    for img_url in images:
        if not download_image(img_url, download_path):
            failed+=1
        count += 1
        percent = percent + 100.0 / no_to_download
        pbar.update(percent)
        if count == no_to_download:
            break

    pbar.finish()
    print "\nDone!\nDownloaded %s images" % (count-failed)
    return
