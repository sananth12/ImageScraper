import sys
from lxml import html
import requests
import urlparse
import os
import argparse
import re
from exceptions import *


def process_links(links, formats=["jpg", "png", "gif", "svg", "jpeg"]):
    x = []
    for l in links:
        if os.path.splitext(l)[1][1:].strip().lower() in formats:
                x.append(l)
    return x


def get_arguments():
    parser = argparse.ArgumentParser(
        description='Downloads images from given URL')
    parser.add_argument('url2scrape', nargs=1, help="URL to scrape")
    parser.add_argument('-m', '--max-images', type=int, default=None,
                        help="Limit on number of images\n")
    parser.add_argument('-s', '--save-dir', type=str, default="images",
                        help="Directory in which images should be saved")
    parser.add_argument('-g', '--injected', help="Scrape injected images",
                        action="store_true")
    parser.add_argument('--max-filesize', type=int, default=100000000,
                        help="Limit on size of image in bytes")
    parser.add_argument('--dump-urls', default=False,
                        help="Print the URLs of the images",
                        action="store_true")
    parser.add_argument('--formats', nargs="*", default=None,
                        help="Specify formats in a list without any separator. This argument must be after the URL.")
    parser.add_argument('--scrape-reverse', default=False,
                        help="Scrape the images in reverse order",
                        action="store_true")
    args = parser.parse_args()
    URL = args.url2scrape[0]
    if not re.match(r'^[a-zA-Z]+://', URL):
        URL = 'http://' + URL
    no_to_download = args.max_images
    save_dir = args.save_dir + '_{uri.netloc}'.format(
        uri=urlparse.urlparse(URL))
    if args.save_dir != "images":
        save_dir = args.save_dir
    download_path = os.path.join(os.getcwd(), save_dir)
    use_ghost = args.injected
    format_list = args.formats if args.formats else ["jpg", "png", "gif", "svg", "jpeg"]
    max_filesize = args.max_filesize
    dump_urls = args.dump_urls
    scrape_reverse = args.scrape_reverse
    return (URL, no_to_download, format_list, download_path, max_filesize,
            dump_urls, scrape_reverse, use_ghost)


def process_download_path(download_path):
    if os.path.exists(download_path):
        if not os.access(download_path, os.W_OK):
            raise DirectoryAccessError
    elif os.access(os.path.dirname(download_path), os.W_OK):
        os.makedirs(download_path)
    else:
        raise DirectoryCreateError
    return True


def get_html(URL, use_ghost):
    if use_ghost:
        URL = urlparse.urljoin("http://", URL)
        import selenium
        import selenium.webdriver
        driver = selenium.webdriver.PhantomJS(service_log_path=os.path.devnull)
        driver.get(URL)
        page_html = driver.page_source
        page_url = driver.current_url
        driver.quit()
    else:
        try:
            page = requests.get(URL)
        except requests.exceptions.MissingSchema:
            URL = "http://" + URL
            page = requests.get(URL)
        finally:
            if page.status_code != 200:
                raise PageLoadError(page.status_code)
            page_html = page.text
            page_url = page.url
    return (page_html, page_url)


def get_img_list(page_html, page_url, format_list):
    tree = html.fromstring(page_html)
    img = tree.xpath('//img/@src')
    links = tree.xpath('//a/@href')
    img_list = process_links(img, format_list)
    img_links = process_links(links, format_list)
    img_list.extend(img_links)
    images = [urlparse.urljoin(page_url, url) for url in img_list]
    images = list(set(images))
    return images


def download_image(img_url, download_path, max_filesize):
    img_request = None
    success_flag = True
    size_success_flag = True
    try:
        img_request = requests.request('get', img_url, stream=True)
        if img_request.status_code != 200:
            raise ImageDownloadError(img_request.status_code)
    except:
        raise ImageDownloadError()

    if img_url[-3:] == "svg" :
        img_content = img_request.content
        with open(os.path.join(download_path,  img_url.split('/')[-1]), 'w') as f:
            f.write(img_content)

    elif int(img_request.headers['content-length']) < max_filesize :
        img_content = img_request.content
        with open(os.path.join(download_path,  img_url.split('/')[-1]), 'w') as f:
            f.write(img_content)
    else:
        raise ImageSizeError(img_request.headers['content-length'])
    return True
