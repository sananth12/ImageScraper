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
+------------------------------------------------------------+
| image-scraper [-h] [--max-images MAX_IMAGES] url_to_scrape |
+------------------------------------------------------------+

Using the tar file:

Extract the contents of the tar file.
Note that ``ImageScraper`` depends on ``lxml``. and ``requests``. 
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

If you dowload the tar:
======================

$cd ImageScraper/
$python setup.py install
$image-scraper [url to scrap]



If installed using pip:
=======================
Open python in terminal.

$image-scraper [url to scrap]



NOTE:
A new folder called "images" will be created in the same place, containing all the downloaded images.


Upgrading
---------

Check and updates and upgrade using:

$ sudo  pip install ImageScraper --upgrade


Issues
------

Q.)All images were not downloaded?
It could be that the content was injected into the page via javascript and this scraper doesn't run javascript.


Todo
----
Scraping sites which inject image tags via javascript by using  PhantomJS or Selenium.

