ImageScraper
============

A cool command line tool which downloads images from the given webpage.

+------------------+--------------------+--------------------+
| Build Status     | Version            | Downloads          |
+==================+====================+====================+
| |Build Status|   | |Latest Version|   | |PyPi downloads|   |
+------------------+--------------------+--------------------+

Demo
^^^^

Click `here <http://showterm.io/d3aef5bc3f37cd49757d1#fast>`__ to see it
in action!

Download
--------

tar file:
~~~~~~~~~

Grab the latest stable build from **- Pip:
https://pypi.python.org/pypi/ImageScraper**

pip install (recommended):
~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also download using pip:

.. code:: sh

    $ pip install ImageScraper

**Dependencies**
^^^^^^^^^^^^^^^^

Note that ``ImageScraper`` depends on ``lxml``, ``requests``,
``setproctitle``, and ``future``. If you run into problems in the
compilation of ``lxml`` through ``pip``, install the ``libxml2-dev`` and
``libxslt-dev`` packages on your system.

Usage
-----

.. code:: sh

    $ image-scraper [OPTIONS] URL

You can also use it in your Python scripts.

.. code:: py

    import image_scraper
    image_scraper.scrape_images(URL)

Options
-------

.. code:: sh

    -h, --help                      Print help
    -m, --max-images <number>       Maximum number images to be scraped
    -s, --save-dir  <path>          Name of the folder to save the images
    -g, --injected                  Scrape injected images
    --formats [ [FORMATS ..]]       Specify the formats of images to be scraped
    --max-filesize  <size>          Limit on size of image in bytes (default: 100000000)
    --dump-urls                     Print the URLs of the images
    --scrape-reverse                Scrape the images in reverse order

If you downloaded the tar:
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract the contents of the tar file.

.. code:: sh

    $ cd ImageScraper/
    $ python setup.py install
    $ image-scraper --max-images 10 [url to scrape]

Examples
--------

Scrape all images

.. code:: sh

    $ image-scraper  ananth.co.in/test.html

Scrape at max 2 images

.. code:: sh

    $ image-scraper -m 2 ananth.co.in/test.html

Scrape only gifs and download to folder ./mygifs

.. code:: sh

    $ image-scraper -s mygifs ananth.co.in/test.html --formats gif

NOTE:
^^^^^

By default, a new folder called "images\_" will be created in the
working directory, containing all the downloaded images.

Issues
------

Q.)All images were not downloaded?

It could be that the content was injected into the page via JavaScript;
this scraper doesn't run JavaScript.

Contribute
----------

If you want to add features, improve them, or report issues, feel free
to send a pull request!!

Contributors
~~~~~~~~~~~~

-  `sananth12 <https://github.com/sananth12>`__ (`Anantha
   Natarajan <http://ananth.co.in>`__)
-  `srirams6 <https://github.com/srirams6>`__ (Sriram Sundarraj)
-  `vigneshmanix <https://github.com/vigneshmanix>`__ (Vignesh M)
-  `osborne6 <https://github.com/osborne6>`__
-  `tsleyson <https://github.com/tsleyson>`__




.. |Build Status| image:: https://travis-ci.org/sananth12/ImageScraper.svg?branch=master
   :target: https://travis-ci.org/sananth12/ImageScraper
.. |Latest Version| image:: https://pypip.in/v/ImageScraper/badge.png
   :target: https://pypi.python.org/pypi/ImageScraper/
.. |PyPi downloads| image:: http://img.shields.io/badge/downloads-8k%20total-blue.svg
   :target: https://pypi.python.org/pypi/ImageScraper
