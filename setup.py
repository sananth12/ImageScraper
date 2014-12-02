#from distutils.core import setup
from setuptools import setup
setup(name='ImageScraper',
      version='2.0.0',
    install_requires=['lxml'],
    author='Anantha Natarajan',
    author_email='sananthanatarajan12@gmail.com',
    packages=['image_scraper'],
    entry_points = {
        'console_scripts': ['image-scraper=image_scraper:console_main'],
        },
    test_suite='tests',
    url='https://github.com/sananth12/ImageScraper/',
    description='A simple image scraper to download all  images from a given url',
      )
