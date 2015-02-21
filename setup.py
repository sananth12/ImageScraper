
from setuptools import setup

setup(name='ImageScraper',
      version='2.0.5',
    install_requires=['lxml', 'requests'],
    author='Anantha Natarajan S',
    author_email='sananthanatarajan12@gmail.com',
    packages=['image_scraper'],
    entry_points = {
        'console_scripts': ['image-scraper=image_scraper:console_main'],
        },
    test_suite='tests',
    url='https://github.com/sananth12/ImageScraper/',
    description='A simple image scraper to download all  images from a given url',
    classifiers=[
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
    ],  
 )
