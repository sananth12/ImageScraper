
import sys
from lxml import html
import requests
import urlparse
import os
from progressbar import *
import argparse


def process_links(links):
    x = []
    for l in links:
        # TODO regular expressions
        if l[-3:] == "jpg" or l[-3:] == "png" or l[-3:] == "gif" or l[-3:] == "svg" :
                x.append(l)
    return x


def console_main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url2scrape', nargs=1, help="URL to scrape")
    parser.add_argument('--max-images', type=int, default=1,
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

    print "\n ImageScraper\n ============\n Requesting page....\n"

    if use_ghost:
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
            page_html= page.text
            page_url = page.url
        except requests.exceptions.MissingSchema:
            URL = "http://" + URL #Default schema is HTTP unless specified
            page = requests.get(URL)
            page_html= page.text
            page_url = page.url

    tree = html.fromstring(page_html)
    img = tree.xpath('//img/@src')
    links = tree.xpath('//a/@href')
    img_links = process_links(links)

    # sub_img = tree.xpath('//descendant-or-self::*[img]/img/@src')

    img.extend(img_links)

    if len(img) == 0:
        sys.exit("Sorry, no images found.")
    
    print "Found %s images: " % len(img)

    no_to_download = args.max_images

    images = [urlparse.urljoin(page_url, url) for url in img]

    #print img
    #print images
    # this does not work if the urls are relative
    for x in range(0, len(img)):
        if img[x][:4] != "http":
            img[x] = "https:" + img[x]

    #Checking if the path exists
    if os.path.exists(download_path):
        if not os.access(os.path.dirname(download_path), os.W_OK):
            #path exists but no write permissions
            sys.exit("Sorry, the directory can't be accessed.")
    elif os.access(os.path.dirname(download_path), os.W_OK):
        #if write permissions are availible, create the directory
        os.makedirs(download_path)
    else:
        sys.exit("Sorry, the directory can't be created.")

    count = 0
    percent = 0.0
    failed = 0
    widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),
               ' ', ETA(), ' ', FileTransferSpeed()]
    pbar = ProgressBar(widgets=widgets, maxval=100).start()

    #print img
    # for img_url in img :
    for img_url in images:
        img_request = None
        try:
            img_request = requests.request('get', img_url)
        except:
            failed += 1
            print "download of %s failed; status code %s" % \
                  (img_url, img_request.status_code)
            # print "Can't download %s"%img_url
            print "status : %s" % img_request.status_code
        f = open(os.path.join(download_path,  img_url.split('/')[-1]), 'w')
        f.write(img_request.content)
        f.close()
        count += 1
        percent = percent + 100.0 / no_to_download
        pbar.update(percent)
        if count == no_to_download:
            break

    pbar.finish()
    print "\nDone!\nDownloaded %s images" % (count-failed)
    return
