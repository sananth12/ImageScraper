ImageScraper :page_with_curl:
============
A high performance, easy to use, multithreaded command line tool which downloads images from the given webpage.

| Build Status | Downloads | Test Coverage |
| ------------ | --------- | ------------- |
| [![Build Status](https://travis-ci.org/sananth12/ImageScraper.svg?branch=master)](https://travis-ci.org/sananth12/ImageScraper) | [![PyPi downloads](http://img.shields.io/badge/downloads-30k%20total-blue.svg)](https://pypi.python.org/pypi/ImageScraper) | [![Coverage Status](https://coveralls.io/repos/sananth12/ImageScraper/badge.svg?branch=coverage)](https://coveralls.io/r/sananth12/ImageScraper?branch=coverage) |

#### Demo
Click [here](http://showterm.io/d3aef5bc3f37cd49757d1#fast) to see it in action!

Download
--------
### tar file:
Grab the latest stable build from **- Pip: [https://pypi.python.org/pypi/ImageScraper](https://pypi.python.org/pypi/ImageScraper)** 

### pip install (recommended):
You can also download using pip:
```sh
$ pip install ImageScraper
``` 
#### **Dependencies**
Note that ``ImageScraper`` depends on ``lxml``, ``requests``, ``setproctitle``, and ``future``. 
If you run into problems in the compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

Usage
-----
```sh
$ image-scraper [OPTIONS] URL
```


You can also use it in your Python scripts. (Deprecated)
```py
import image_scraper
image_scraper.scrape_images(URL)
```

Options
-------
```sh
-h, --help            show this help message and exit
-m MAX_IMAGES, --max-images MAX_IMAGES
                    Limit on number of images
-s SAVE_DIR, --save-dir SAVE_DIR
                    Directory in which images should be saved
-g, --injected        Scrape injected images
--proxy-server PROXY_SERVER
                    Proxy server to use
--min-filesize MIN_FILESIZE
                    Limit on size of image in bytes
--max-filesize MAX_FILESIZE
                    Limit on size of image in bytes
--dump-urls           Print the URLs of the images
--formats [FORMATS [FORMATS ...]]
                    Specify formats in a list without any separator. This
                    argument must be after the URL.
--scrape-reverse      Scrape the images in reverse order
--filename-pattern FILENAME_PATTERN
                    Only scrape images with filenames that match the given
                    regex pattern
--nthreads NTHREADS   The number of threads to use when downloading images.
```

### If you downloaded the tar:
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

#### NOTE:
By default, a new folder called "images_<domain>" will be created in the working directory, containing all the downloaded images.




Issues
------

Q.)All images were not downloaded?

It could be that the content was injected into the page via JavaScript; this scraper doesn't run JavaScript. 
 

Contribute
----------
If you want to add features, improve them, or report issues, feel free to send a pull request!!

### Contributors

- [sananth12](https://github.com/sananth12) ([Anantha Natarajan](http://ananth.co.in))
- [ssundarraj](https://github.com/ssundarraj) (Sriram Sundarraj)
- [vigneshmanix](https://github.com/vigneshmanix) (Vignesh M) 
- [osborne6](https://github.com/osborne6)
- [tsleyson](https://github.com/tsleyson)
- [joshwget](https://github.com/joshwget)
- [dannyflax](https://github.com/dannyflax)

Disclaimer
----------

ImageScraper is to be used education/research purposes only. The authors takes NO responsibility and/or liability for how you choose to use any of the tools/source code/any files provided. By using ImageScraper, you understand that you are AGREEING TO USE AT YOUR OWN RISK.


License
-------
![GPL V3](https://raw.githubusercontent.com/sananth12/ImageScraper/master/images/gpl.png)


[![Analytics](https://ga-beacon.appspot.com/UA-60764448-1/ImageScraper/README.md)](https://github.com/igrigorik/ga-beacon)
