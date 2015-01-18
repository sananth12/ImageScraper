import sys
from lxml import html
import requests
import urlparse
import os
from progressbar import *
import argparse

def process_links(links, formats=["jpg", "png", "gif", "svg"]):
    x = []
    for l in links:
        # TODO regular expressions
        if l[-3:] in formats:
                x.append(l)
    return x

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('url2scrape', nargs=1, help="URL to scrape")
    parser.add_argument('--max-images', type=int, default=0,
                        help="Limit on number of images")
    parser.add_argument('-s', '--save-dir', type=str, default="images",
                        help="Directory in which images should be saved")
    parser.add_argument('-g', '--injected', help="scrape injected images",
                        action="store_true")
    args = parser.parse_args()
    URL = args.url2scrape[0]
    no_to_download = args.max_images
    save_dir = args.save_dir
    download_path = os.path.join(os.getcwd(), save_dir)
    use_ghost = args.injected
    return (URL, no_to_download, download_path, use_ghost)

def process_download_path(download_path):
    if os.path.exists(download_path):
        if not os.access(download_path, os.W_OK):
            sys.exit("Sorry, the directory can't be accessed.")
    elif os.access(os.path.dirname(download_path), os.W_OK):
        os.makedirs(download_path)
    else:
        sys.exit("Sorry, the directory can't be created.")

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
            page_html= page.text
            page_url = page.url
    return (page_html, page_url)

def get_img_list(page_html, page_url):
    tree = html.fromstring(page_html)
    img = tree.xpath('//img/@src')
    links = tree.xpath('//a/@href')
    img_links = process_links(links)
    img_list = process_links(img)
    img_list.extend(img_links)
    images = [urlparse.urljoin(page_url, url) for url in img_list]
    return images

def download_image(img_url, download_path):
    img_request = None
    success_flag=True
    try:
        img_request = requests.request('get', img_url)
    except:
        success_flag=False
        print "download of %s failed; status code %s" % \
              (img_url, img_request.status_code)
        print "status : %s" % img_request.status_code
    f = open(os.path.join(download_path,  img_url.split('/')[-1]), 'w')
    f.write(img_request.content)
    f.close()
    return success_flag
