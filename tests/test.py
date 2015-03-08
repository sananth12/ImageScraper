#testset.py
#yet to write proper tests.
# TEST 1: Check if 3 images are dowloaded from ananth.co.in/test.html
from nose.tools import eq_

def test_sum():
    eq_(2+2,4)

def test_get_html_200():
	import requests
	r=requests.get('http://ananth.co.in/test.html')
	actual_html=u'<html>\n\n<head>\n    \n</head>\n\n<body>\n<img src="images/test1.jpg"/>\n<img src="images/test.png"/>\n<img src="images/test4.gif"/>\n</body>\n    \n</html>\n'
	eq_(r.text, actual_html)

def test_get_html_404():
	import requests
	r=requests.get('http://ananth.co.in/test404.html')
	eq_(r.status_code, 404)
