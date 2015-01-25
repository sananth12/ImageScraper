ImageScraper
============
A simple python script which downloads all images in the given webpage.


Download
--------
tar file:
Grab the latest build using https://pypi.python.org/pypi/ImageScraper 

pip install:
$pip install ImageScraper

 
Usage
-----
+----------------------------------------------------------------------+
| image-scraper [-h] [--max-images MAX_IMAGES] [-g] [-f] url_to_scrape |
+----------------------------------------------------------------------+

Using the tar file:

Extract the contents of the tar file.
Note that ``ImageScraper`` depends on ``lxml``. and ``requests``. 
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

If you dowload the tar:
======================

$cd ImageScraper/
$python setup.py install
$image-scraper --max-images 50 [url to scrape]


If installed using pip:
=======================
Open python in terminal.

$image-scraper --max-images 5 [url to scrape]



NOTE:
A new folder called "images" will be created in the same place, containing all the downloaded images.


Upgrading
---------

Check and updates and upgrade using:

$ sudo  pip install ImageScraper --upgrade


