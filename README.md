ImageScraper
============
First python app :D
A simple python script which downloads all images in the given webpage.

| Build Status | Version | Downloads |
| ------------ | ------- | ------------------- |
| [![Build Status](https://travis-ci.org/sananth12/ImageScraper.svg?branch=master)](https://travis-ci.org/sananth12/ImageScraper) |  [![Latest Version](https://pypip.in/v/ImageScraper/badge.png)](https://pypi.python.org/pypi/ImageScraper/) | [![PyPi downloads](https://pypip.in/d/ImageScraper/badge.png)](https://crate.io/packages/ImageScraper/) |


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
###If you downloaded the tar:
Extract the contents of the tar file.
Note that ``ImageScraper`` depends on ``lxml``. and ``requests``. 
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

```sh
$cd ImageScraper/image_scraper/
$python __init__.py
$ Enter URL to scrap: https://github.com
$ Found 6 images:
$ How many images do you want ? : 6
$ Done.
```

###If installed using pip:
Open python in terminal.

```sh
$python
>>>import image_scraper
   Enter URL to scrap: https://github.com
   Found 6 images:
   How many images do you want ? : 6
    Done.
```


####NOTE:
A new folder called "images" will be created in the same place, containing all the downloaded images.

Issues
------

Q.)All images were not downloaded?

It could be that the content was injected into the page via javascript and this scraper doesn't run javascript. 
 

Todo
----
Scraping sites which inject image tags via javascript using PhantomJS or Selenium.
