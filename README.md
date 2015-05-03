ImageScraper :page_with_curl:
============
A high performance, easy to use, multithreaded command line tool which downloads images from the given webpage.

| Build Status | Version | Downloads | Test Coverage |
| ------------ | ------- | --------- | ------------- |
| [![Build Status](https://travis-ci.org/sananth12/ImageScraper.svg?branch=master)](https://travis-ci.org/sananth12/ImageScraper) |  [![Latest Version](https://pypip.in/v/ImageScraper/badge.png)](https://pypi.python.org/pypi/ImageScraper/) | [![PyPi downloads](http://img.shields.io/badge/downloads-10k%20total-blue.svg)](https://pypi.python.org/pypi/ImageScraper) | [![Coverage Status](https://coveralls.io/repos/sananth12/ImageScraper/badge.svg?branch=coverage)](https://coveralls.io/r/sananth12/ImageScraper?branch=coverage) |

####Demo
Click [here](http://showterm.io/d3aef5bc3f37cd49757d1#fast) to see it in action!

Download
--------
###tar file:
Grab the latest stable build from **- Pip: [https://pypi.python.org/pypi/ImageScraper](https://pypi.python.org/pypi/ImageScraper)** 

###pip install (recommended):
You can also download using pip:
```sh
$ pip install ImageScraper
``` 
####**Dependencies**
Note that ``ImageScraper`` depends on ``lxml``, ``requests``, ``setproctitle``, and ``future``. 
It also depends on `pyThreadpool` which can be downloaded and installed from [here](http://github.com/srirams6/py-Threadpool) temporarily.
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

Usage
-----
```sh
$ image-scraper [OPTIONS] URL
```
You can also use it in your Python scripts.
```py
import image_scraper
image_scraper.scrape_images(URL)
```

Options
-------
```sh
-h, --help                      Print help
-m, --max-images <number>       Maximum number images to be scraped
-s, --save-dir	<path>          Name of the folder to save the images
-g, --injected                  Scrape injected images
--formats [ [FORMATS ..]]       Specify the formats of images to be scraped
--max-filesize	<size>          Limit on size of image in bytes (default: 100000000)
--dump-urls                     Print the URLs of the images
--scrape-reverse                Scrape the images in reverse order
--proxy-urls			Use the specified HTTP/HTTPS proxy
```

###If you downloaded the tar:
Extract the contents of the tar file.


```sh
$ cd ImageScraper/
$ python setup.py install
$ image-scraper --max-images 10 [url to scrape]

```

Examples
--------

Scrape all images 
```sh
$ image-scraper  ananth.co.in/test.html
```

Scrape at max 2 images
```sh
$ image-scraper -m 2 ananth.co.in/test.html
```

Scrape only gifs and download to folder ./mygifs
```sh
$ image-scraper -s mygifs ananth.co.in/test.html --formats gif
```

####NOTE:
By default, a new folder called "images_<domain>" will be created in the working directory, containing all the downloaded images.


Issues
------

Q.)All images were not downloaded?

It could be that the content was injected into the page via JavaScript; this scraper doesn't run JavaScript. 
 

Contribute
----------
If you want to add features, improve them, or report issues, feel free to send a pull request!!

###Contributors

- [sananth12](https://github.com/sananth12) ([Anantha Natarajan](http://ananth.co.in))
- [srirams6](https://github.com/srirams6) (Sriram Sundarraj)
- [vigneshmanix](https://github.com/vigneshmanix) (Vignesh M) 
-	[osborne6](https://github.com/osborne6)
- [tsleyson](https://github.com/tsleyson)

[![Throughput Graph](https://graphs.waffle.io/sananth12/ImageScraper/throughput.svg)](https://waffle.io/sananth12/ImageScraper/metrics)

License
-------
![GPL V3](https://raw.githubusercontent.com/sananth12/ImageScraper/master/images/gpl.png)


[![Analytics](https://ga-beacon.appspot.com/UA-60764448-1/ImageScraper/README.md)](https://github.com/igrigorik/ga-beacon)
