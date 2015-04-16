from future.standard_library import install_aliases
install_aliases()
import sys
from lxml import html
import requests
from urllib.parse import urlparse, urljoin
from past.utils import old_div
import os
import argparse
import re
from image_scraper.exceptions import *
import threading

class ImageScraper(object):
    url = None
    no_to_download = 0
    format_list = []
    download_path = "images"
    max_filesize = 100000000
    dump_urls = False
    scrape_reverse = False
    use_ghost = False
    page_html = None
    page_url = None
    images = None
    proxy_url = None
    proxies = {}

    def __init__(self):
        url = None
        no_to_download = 0
        format_list = []
        download_path = "images"
        max_filesize = 100000000
        dump_urls = False
        scrape_reverse = False
        use_ghost = False
        images = None

    def get_arguments(self):
        parser = argparse.ArgumentParser(
            description='Downloads images from given URL')
        parser.add_argument('url2scrape', nargs=1, help="URL to scrape")
        parser.add_argument('-m', '--max-images', type=int, default=None,
                            help="Limit on number of images\n")
        parser.add_argument('-s', '--save-dir', type=str, default="images",
                            help="Directory in which images should be saved")
        parser.add_argument('-g', '--injected', help="Scrape injected images",
                            action="store_true")
        parser.add_argument('--proxy-server', type=str, default=None,
                            help="Proxy server to use")
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
        self.url = args.url2scrape[0]
        if not re.match(r'^[a-zA-Z]+://', self.url):
            self.url = 'http://' + self.url
        self.no_to_download = args.max_images
        save_dir = args.save_dir + '_{uri.netloc}'.format(
            uri=urlparse(self.url))
        if args.save_dir != "images":
            save_dir = args.save_dir
        self.download_path = os.path.join(os.getcwd(), save_dir)
        self.use_ghost = args.injected
        self.format_list = args.formats if args.formats else [
            "jpg", "png", "gif", "svg", "jpeg"]
        self.max_filesize = args.max_filesize
        self.dump_urls = args.dump_urls
        self.proxy_url = args.proxy_server
        self.proxies = {}
        if self.proxy_url:
            if not re.match(r'^[a-zA-Z]+://', self.proxy_url):
                self.proxy_url = 'http://' + self.proxy_url
            proxy_start_length = self.proxy_url.find("://") + 3
            self.proxies = {
                self.proxy_url[:(proxy_start_length - 3)]: self.proxy_url
            }

        self.scrape_reverse = args.scrape_reverse
        return (self.url, self.no_to_download, self.format_list, self.download_path, self.max_filesize,
                self.dump_urls, self.scrape_reverse, self.use_ghost)

    def get_html(self):
        if self.use_ghost:
            self.url = urljoin("http://", self.url)
            import selenium
            import selenium.webdriver
            driver = selenium.webdriver.PhantomJS(
                service_log_path=os.path.devnull)
            driver.get(self.url)
            page_html = driver.page_source
            page_url = driver.current_url
            driver.quit()
        else:
            if self.proxy_url:
                print("Using proxy: " + self.proxy_url + "\n")
            try:
                page = requests.get(self.url, proxies=self.proxies)
                if page.status_code != 200:
                    raise PageLoadError(page.status_code)
            except requests.exceptions.MissingSchema:
                self.url = "http://" + self.url
                page = requests.get(self.url, proxies=self.proxies)
                if page.status_code != 200:
                    raise PageLoadError(page.status_code)
            finally:
                page_html = page.text
                page_url = page.url

        self.page_html = page_html
        self.page_url = page_url
        return (self.page_html, self.page_url)

    def get_img_list(self):
        tree = html.fromstring(self.page_html)
        img = tree.xpath('//img/@src')
        links = tree.xpath('//a/@href')
        img_list = self.process_links(img)
        img_links = self.process_links(links)
        img_list.extend(img_links)
        images = [urljoin(self.url, img_url) for img_url in img_list]
        images = list(set(images))
        self.images = images
        if self.scrape_reverse:
            self.images.reverse()
        return self.images

    def process_download_path(self):
        if os.path.exists(self.download_path):
            if not os.access(self.download_path, os.W_OK):
                raise DirectoryAccessError
        elif os.access(os.path.dirname(self.download_path), os.W_OK):
            os.makedirs(self.download_path)
        else:
            raise DirectoryCreateError
        return True

    def download_image(self, img_url):
        img_request = None
        success_flag = True
        size_success_flag = True
        try:
            img_request = requests.request(
                'get', img_url, stream=True, proxies=self.proxies)
            if img_request.status_code != 200:
                raise ImageDownloadError(img_request.status_code)
        except:
            raise ImageDownloadError()

        if img_url[-3:] == "svg" or int(img_request.headers['content-length']) < self.max_filesize:
            img_content = img_request.content
            with open(os.path.join(self.download_path,  img_url.split('/')[-1]), 'wb') as f:
                byte_image = bytes(img_content)
                f.write(byte_image)
        else:
            raise ImageSizeError(img_request.headers['content-length'])
        return True

    def process_links(self, links):
        x = []
        for l in links:
            if os.path.splitext(l)[1][1:].strip().lower() in self.format_list:
                x.append(l)
        return x


def download_worker_fn(scraper, img_url, pbar, status_flags, status_lock):
    failed = False
    size_failed = False
    try:
        scraper.download_image(img_url)
    except ImageDownloadError:
        failed = True
    except ImageSizeError:
        size_failed = True
    status_lock.acquire(True)
    if failed:
        status_flags['failed'] += 1
    elif size_failed:
        status_flags['over_max_filesize'] += 1
    status_flags['percent'] = status_flags[
        'percent'] + old_div(100.0, scraper.no_to_download)
    pbar.update(status_flags['percent'] % 100)
    status_lock.release()
    return True
