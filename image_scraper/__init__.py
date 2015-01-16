
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
                        help="URL to scrape")
    args = parser.parse_args()

    URL = args.url2scrape[0]

    page = requests.get(URL)

    tree = html.fromstring(page.text)

    img = tree.xpath('//img/@src')

    links = tree.xpath('//a/@href')

    img_links = process_links(links)

    # sub_img = tree.xpath('//descendant-or-self::*[img]/img/@src')

    img.extend(img_links)

    if len(img) == 0:
        sys.exit("Sorry, no images found")
    print "\n ImageScraper\n ============\n"
    print "Found %s images: " % len(img)

    no_to_download = args.max_images

    images = [urlparse.urljoin(page.url, url) for url in img]
    print img
    #print images
    # this does not work if the urls are relative
    for x in range(0, len(img)):
        if img[x][:4] != "http":
            img[x] = "https:" + img[x]

    if not os.path.exists('images'):
        os.makedirs('images')

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
        f = open('images/%s' % img_url.split('/')[-1], 'w')
        f.write(img_request.content)
        f.close()
        count += 1
        percent = 100.0* (count / len(img))
        pbar.update(percent)
        if count == no_to_download:
            break

    pbar.finish()
    print "\nDone!\nDownloaded %s images" % (count-failed)
    return
