
import sys
from progressbar import *
from utils import (process_links, get_html, get_img_list, download_image,
                   process_download_path, get_arguments)


def console_main():
    URL, no_to_download, format_list, download_path, max_filesize, dump_urls, use_ghost = get_arguments()
    print "\nImageScraper\n============\nRequesting page....\n"

    page_html, page_url = get_html(URL, use_ghost)
    images = get_img_list(page_html, page_url, format_list)

    if len(images) == 0:
        sys.exit("Sorry, no images found.")
    if no_to_download == 0:
        no_to_download = len(images)

    print "Found %s images: " % len(images)

    process_download_path(download_path)

    for img_url in images:
        if dump_urls:
            print img_url

    count = 0
    percent = 0.0
    failed = 0
    over_max_filesize = 0
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=100).start()

    for img_url in images:
        flag, size_flag = download_image(img_url, download_path, max_filesize)
        if not flag:
            if not size_flag:
                failed += 1
            else:
                over_max_filesize += 1
        count += 1
        percent = percent + 100.0 / no_to_download
        pbar.update(percent % 100)
        if count == no_to_download:
            break

    pbar.finish()
    print "\nDone!\nDownloaded %s images" % (count-failed-over_max_filesize)
    return
