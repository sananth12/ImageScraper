def console_main():
    import sys
    from progressbar import *
    from utils import (process_links, get_html, get_img_list,
                       download_image, process_download_path, get_arguments)
    URL, no_to_download, format_list, download_path, max_filesize, dump_urls, scrape_reverse, use_ghost = get_arguments()
    print "\nImageScraper\n============\nRequesting page....\n"

    page_html, page_url = get_html(URL, use_ghost)
    images = get_img_list(page_html, page_url, format_list)

    if len(images) == 0:
        sys.exit("Sorry, no images found.")
    if no_to_download == 0:
        no_to_download = len(images)

    print "Found %s images: " % len(images)

    download_path_flag, download_path_msg =
    process_download_path(download_path)
    if not download_path_flag:
        sys.exit(download_path_msg)

    if scrape_reverse:
        images.reverse()

    if dump_urls:
        for img_url in images:
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


def scrape_images(url, no_to_download=0,
                  format_list=["jpg", "png", "gif", "svg", "jpeg"],
                  download_path='images', max_filesize=100000000,
                  dump_urls=False, use_ghost=False):
    import sys
    import os
    from utils import (process_links, get_html, get_img_list, download_image,
                       process_download_path, get_arguments)
    page_html, page_url = get_html(url, use_ghost)
    images = get_img_list(page_html, page_url, format_list)

    download_path = os.path.join(os.getcwd(), download_path)

    if len(images) == 0:
        return
    if no_to_download == 0:
        no_to_download = len(images)

    download_path_flag, download_path_msg = process_download_path(download_path)
    if not download_path_flag:
        sys.exit(download_path_msg)

    count = 0
    failed = 0
    over_max_filesize = 0

    for img_url in images:
        flag, size_flag = download_image(img_url, download_path, max_filesize)
        if not flag:
            if not size_flag:
                failed += 1
            else:
                over_max_filesize += 1
        count += 1
        if count == no_to_download:
            break
    return count, failed
