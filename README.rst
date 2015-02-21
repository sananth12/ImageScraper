ImageScraper 
=============

A cool command line tool which downloads all images in the given
webpage.

+------------------+--------------------+--------------------+
| Build Status     | Version            | Downloads          |
+==================+====================+====================+
| |Build Status|   | |Latest Version|   | |PyPi downloads|   |
+------------------+--------------------+--------------------+

Download
--------

pip install(recommended)
~~~~~~~~~~~~~~~~~~~~~~~~

You can also download using pip:

.. code:: sh

    $ pip install ImageScraper

**Dependencies**
^^^^^^^^^^^^^^^^

Note that ``ImageScraper`` depends on ``lxml`` and ``requests``. If you
run into problems in the compilation of ``lxml`` through ``pip``,
install the ``libxml2-dev`` and ``libxslt-dev`` packages on your system.

Usage
-----

.. code:: sh

    $ image-scraper [OPTIONS] URL

Options
-------

.. code:: sh

    -h, --help                      Print help
    -m, --max-images <number>       Maximum number images to be scraped
    -s, --save-dir  <path>          Name of the folder to save the images (default: ./images_<domain>)
    --max-filesize  <size>          Limit on size of image in bytes (default: 100000000)
    --dump-urls                     Print the URLs of the images

If you downloaded the tar:
~~~~~~~~~~~~~~~~~~~~~~~~~~

Extract the contents of the tar file.

.. code:: sh

    $cd ImageScraper/
    $python setup.py install
    $image-scraper --max-images 10 [url to scrape]

If installed using pip:
~~~~~~~~~~~~~~~~~~~~~~~

Open python in terminal.

.. code:: sh

    $image-scraper --max-images 10 [url to scrape]

NOTE:
^^^^^

A new folder called "images\_" will be created in the same place,
containing all the downloaded images.

Upgrading
---------

Check if a newer version if available and upgrade using:

.. code:: sh

    $ sudo  pip install ImageScraper --upgrade


.. |Build Status| image:: https://travis-ci.org/sananth12/ImageScraper.svg?branch=travis-branch
   :target: https://travis-ci.org/sananth12/ImageScraper
.. |Latest Version| image:: https://pypip.in/v/ImageScraper/badge.png
   :target: https://pypi.python.org/pypi/ImageScraper/
.. |PyPi downloads| image:: http://img.shields.io/badge/downloads-7k%20total-blue.svg
   :target: https://pypi.python.org/pypi/ImageScraper
