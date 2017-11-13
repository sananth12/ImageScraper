""" Contains ImageScraper class and utility functions. """

from future.standard_library import install_aliases
install_aliases()
from lxml import html
import requests
from urllib.parse import urlparse, urljoin
from past.utils import old_div
import os
import argparse
import re
from .exceptions import PageLoadError, DirectoryAccessError,\
                        DirectoryCreateError, ImageDownloadError, ImageSizeError


class ImageScraper(object):
    """ Scraper class. """
    def __init__(self):
        self.url = None
        self.no_to_download = 0
        self.format_list = []
        self.download_path = "images"
        self.min_filesize = 0
        self.max_filesize = 100000000
        self.dump_urls = False
        self.scrape_reverse = False
        self.use_ghost = False
        self.images = None
        self.nthreads = 10
        self.filename_pattern = None
        self.page_html = None
        self.page_url = None
        self.proxy_url = None
        self.proxies = {}

    def get_arguments(self):
        """ Gets the arguments from the command line. """

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
        parser.add_argument('--min-filesize', type=int, default=0,
                            help="Limit on size of image in bytes")
        parser.add_argument('--max-filesize', type=int, default=100000000,
                            help="Limit on size of image in bytes")
        parser.add_argument('--dump-urls', default=False,
                            help="Print the URLs of the images",
                            action="store_true")
        parser.add_argument('--formats', nargs="*", default=None,
                            help="Specify formats in a list without any separator.\
                                  This argument must be after the URL.")
        parser.add_argument('--scrape-reverse', default=False,
                            help="Scrape the images in reverse order",
                            action="store_true")
        parser.add_argument('--filename-pattern', type=str, default=None,
                            help="Only scrape images with filenames that\
                                  match the given regex pattern")
        parser.add_argument('--nthreads', type=int, default=10,
                            help="The number of threads to use when downloading images.")
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
        self.min_filesize = args.min_filesize
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
        self.filename_pattern = args.filename_pattern
        self.nthreads = args.nthreads
        return (self.url, self.no_to_download, self.format_list,
                self.download_path, self.min_filesize, self.max_filesize,
                self.dump_urls, self.scrape_reverse, self.use_ghost, self.filename_pattern)

    def get_html(self):
        """ Downloads HTML content of page given the page_url"""

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
            except requests.exceptions.ConnectionError:
                raise PageLoadError(None)
            try:
                page_html = page.text
                page_url = page.url
            except UnboundLocalError:
                raise PageLoadError(None)

        self.page_html = page_html
        self.page_url = page_url
        return (self.page_html, self.page_url)

    def get_img_list(self):
        """ Gets list of images from the page_html. """
        tree = html.fromstring(self.page_html)
        img = tree.xpath('//img/@src')
        links = tree.xpath('//a/@href')
        img_list = self.process_links(img)
        img_links = self.process_links(links)
        img_list.extend(img_links)

        if self.filename_pattern:
            # Compile pattern for efficiency
            pattern = re.compile(self.filename_pattern)

            # Verifies filename in the image URL matches pattern
            def matches_pattern(img_url):
                """ Function to check if pattern is matched. """

                img_filename = urlparse(img_url).path.split('/')[-1]
                return pattern.search(img_filename)

            images = [urljoin(self.url, img_url) for img_url in img_list
                      if matches_pattern(img_url)]
        else:
            images = [urljoin(self.url, img_url) for img_url in img_list]

        images = list(set(images))
        self.images = images
        if self.scrape_reverse:
            self.images.reverse()
        return self.images

    def process_download_path(self):
        """ Processes the download path.

            It checks if the path exists and the scraper has
            write permissions.
        """
        if os.path.exists(self.download_path):
            if not os.access(self.download_path, os.W_OK):
                raise DirectoryAccessError
        elif os.access(os.path.dirname(self.download_path), os.W_OK):
            os.makedirs(self.download_path)
        else:
            raise DirectoryCreateError
        return True

    def download_image(self, img_url):
        """ Downloads a single image.

            Downloads img_url using self.page_url as base.
            Also, raises the appropriate exception if required.
        """
        img_request = None
        try:
            img_request = requests.request(
                'get', img_url, stream=True, proxies=self.proxies)
            if img_request.status_code != 200:
                raise ImageDownloadError(img_request.status_code)
        except:
            raise ImageDownloadError()

        if img_url[-3:] == "svg" or (int(img_request.headers['content-length']) > self.min_filesize and\
                                     int(img_request.headers['content-length']) < self.max_filesize):
            img_content = img_request.content
            with open(os.path.join(self.download_path, img_url.split('/')[-1]), 'wb') as f:
                byte_image = bytes(img_content)
                f.write(byte_image)
        else:
            raise ImageSizeError(img_request.headers['content-length'])
        return True

    def process_links(self, links):
        """ Function to process the list of links and filter required links."""
        links_list = []
        for link in links:
            if os.path.splitext(link)[1][1:].strip().lower() in self.format_list:
                links_list.append(link)
        return links_list


def download_worker_fn(scraper, img_url, pbar, status_flags, status_lock):
    """ Stnadalone function that downloads images. """
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
        status_flags['under_min_or_over_max_filesize'] += 1
    status_flags['percent'] = status_flags[
        'percent'] + old_div(100.0, scraper.no_to_download)
    pbar.update(status_flags['percent'] % 100)
    status_lock.release()
    return True
