import sys
from lxml import html
import requests
import urlparse
import os
import argparse
import re


def process_links(links, formats=["jpg", "png", "gif", "svg", "jpeg"]):
    x = []
    for l in links:
        if os.path.splitext(l)[1][1:].strip().lower() in formats:
                x.append(l)
    return x


def get_arguments():
    parser = argparse.ArgumentParser(description='Dowloads images form given URL')
    parser.add_argument('url2scrape', nargs=1, help="URL to scrape")
    parser.add_argument('-m', '--max-images', type=int, default=0,
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
    args = parser.parse_args()
    URL = args.url2scrape[0]
    if not re.match(r'^[a-zA-Z]+://', URL):
        URL = 'http://' + URL
    no_to_download = args.max_images
    save_dir = args.save_dir + '_{uri.netloc}'.format(uri=urlparse.urlparse(URL))
    if args.save_dir != "images":
        save_dir = args.save_dir
    download_path = os.path.join(os.getcwd(), save_dir)
    use_ghost = args.injected
    format_list = ["jpg", "png", "gif", "svg", "jpeg"]
    max_filesize = args.max_filesize
    dump_urls = args.dump_urls
    return (URL, no_to_download, format_list, download_path, max_filesize,
            dump_urls, use_ghost)


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
    except:
        success_flag = False
        print "download of %s failed; status code %s" % \
              (img_url, img_request.status_code)
        print "status : %s" % img_request.status_code
        return success_flag
    if int(img_request.headers['content-length']) < max_filesize:
        img_content = img_request.content
        f = open(os.path.join(download_path,  img_url.split('/')[-1]), 'w')
        f.write(img_content)
        f.close()
    else:
        success_flag = False
        size_success_flag = False
    return success_flag, size_success_flag
