# testset.py
# yet to write proper tests.
# TEST 1: Check if 3 images are dowloaded from ananth.co.in/test.html
from nose.tools import eq_, ok_
from image_scraper.utils import *
from image_scraper.exceptions import *


def test_sum():
    eq_(2+2, 4)


def test_get_html_200():
    page_html, url = get_html('http://ananth.co.in/test.html', False)
    actual_html = u'<html>\n\n<head>\n    \n</head>\n\n<body>\n<img src="images/test1.jpg"/>\n<img src="images/test.png"/>\n<img src="images/test4.gif"/>\n</body>\n    \n</html>\n'
    eq_(page_html, actual_html)


def test_get_html_404():
    try:
        page_html, url = get_html('ananth.co.in/test404.html', False)
        eq_(2, 3, "Page loaded with 200.")  # If the page loads, the test fails.
    except PageLoadError as e:
        eq_(e.status_code, 404)


def test_process_links():
    links = ['a.png', 'b.png', 'c.jpg', 'd.gif', 'f.svg', 'g.svg']
    r = process_links(links, formats=["jpg", "png", "gif", "jpeg"])
    correct_res = ['a.png', 'b.png', 'c.jpg', 'd.gif']
    eq_(r, correct_res)
