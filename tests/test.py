import os
import sys
import threading
import image_scraper
import SimplePool
import glob
from nose.tools import eq_, ok_
from image_scraper.utils import *
from image_scraper.exceptions import *
from image_scraper.progressbar import *

def test_sum():
    eq_(2+2, 4)


def test_get_html_200():
    eq_(2+2, 4)
    scraper = ImageScraper()
    scraper.url = 'http://ananth.co.in/test.html'
    scraper.get_html()
    actual_html = u'<html>\n\n<head>\n    \n</head>\n\n<body>\n<img src="images/test4.gif"/>\n<img src="images/test1.jpg"/>\n<img src="images/build.svg"/>\n<img src="images/test.png"/>\n\n</body>\n    \n</html>\n'
    eq_(scraper.page_html, actual_html)


def test_get_html_404():
    try:
        scraper = ImageScraper()
        scraper.url = 'ananth.co.in/test404.html'
        scraper.get_html()
        eq_(2, 3, "Page loaded with 200.")  # If the page loads, the test fails.
    except PageLoadError as e:
        eq_(e.status_code, 404)


def test_process_links():
    scraper = ImageScraper()
    scraper.url = 'http://ananth.co.in/test.html'
    scraper.format_list = ["jpg", "png", "gif", "jpeg"]
    links = ['a.png', 'b.png', 'c.jpg', 'd.gif', 'f.svg', 'g.svg']
    r = scraper.process_links(links)
    correct_res = ['a.png', 'b.png', 'c.jpg', 'd.gif']
    eq_(r, correct_res)


def test_process_links_empty():
    scraper = ImageScraper()
    scraper.url = 'http://ananth.co.in/test.html'
    scraper.format_list = []
    links = ['a.png', 'b.png', 'c.jpg', 'd.gif', 'f.svg', 'g.svg']
    r = scraper.process_links(links)
    correct_res = []
    eq_(r, correct_res)


def test_get_img_list():
    scraper = ImageScraper()
    scraper.page_html = u'<html>\n\n<head>\n\n</head>\n\n<body>\n<img src="images/test4.gif"/>\n<img src="images/test1.jpg"/>\n<img src="images/build.svg"/>\n<img src="images/test.png"/>\n\n</body>\n\n</html>\n'
    scraper.format_list = ["jpg", "png", "gif", "jpeg", "svg"]
    scraper.url = 'ananth.co.in/test.html'
    img_list = scraper.get_img_list()
    actual_list = ['ananth.co.in/images/build.svg', 'ananth.co.in/images/test4.gif', 'ananth.co.in/images/test1.jpg', 'ananth.co.in/images/test.png']
    eq_(sorted(img_list), sorted(actual_list))

def test_get_img_list_with_pattern():
    scraper = ImageScraper()
    scraper.page_html = u'<html>\n\n<head>\n\n</head>\n\n<body>\n<img src="images/test4.gif"/>\n<img src="images/test1.jpg"/>\n<img src="images/build.svg"/>\n<img src="images/test.png"/>\n\n</body>\n\n</html>\n'
    scraper.format_list = ["jpg", "png", "gif", "jpeg", "svg"]
    scraper.url = 'ananth.co.in/test.html'
    scraper.filename_pattern = '[0-9]'
    img_list = scraper.get_img_list()
    actual_list = ['ananth.co.in/images/test4.gif', 'ananth.co.in/images/test1.jpg']
    eq_(sorted(img_list), sorted(actual_list))
