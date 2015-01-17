ImageScraper :page_with_curl:
============
A simple python script which downloads all images in the given webpage.

| Build Status | Version | Downloads |
| ------------ | ------- | ------------------- |
| [![Build Status](https://travis-ci.org/sananth12/ImageScraper.svg?branch=master)](https://travis-ci.org/sananth12/ImageScraper) |  [![Latest Version](https://pypip.in/v/ImageScraper/badge.png)](https://pypi.python.org/pypi/ImageScraper/) | [![PyPi downloads](http://img.shields.io/badge/downloads-6587%20total-blue.svg)](https://pypi.python.org/pypi/ImageScraper) |


Download
--------
###tar file:
Grab the latest build using **- Pip: [https://pypi.python.org/pypi/ImageScraper](https://pypi.python.org/pypi/ImageScraper)** 

###pip install
You can also download using pip:
```sh
$ pip install ImageScraper
``` 

Usage
-----
```sh
image-scraper [-h] [--max-images MAX_IMAGES] url2scrape
```

###If you downloaded the tar:
Extract the contents of the tar file.
Note that ``ImageScraper`` depends on ``lxml``. and ``requests``. 
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.


```sh
$cd ImageScraper/
$python setup.py install
$image-scraper --max-images 10 [url to scrape]

```

###If installed using pip:
Open python in terminal.

```sh
$image-scraper --max-images 10 [url to scrape]

```


####NOTE:
A new folder called "images" will be created in the same place, containing all the downloaded images.


Upgrading
---------

Check if a newer version if available  and upgrade using:

```sh
$ sudo  pip install ImageScraper --upgrade
```

Issues
------

Q.)All images were not downloaded?

It could be that the content was injected into the page via javascript and this scraper doesn't run javascript. 
 

Todo
----
Scraping sites which inject image tags via javascript, by using PhantomJS or Selenium.


Contribute
----------
If you want to add features, improve them, or report issues, feel free to send a pull request!!

Special thanks to @osborne6 for making a proper CLI.  :)