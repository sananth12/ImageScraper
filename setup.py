from distutils.core import setup
setup(name='ImageScraper',
      version='1.0.3',
    install_requires=['lxml'],
    author='Anantha Natarajan',
    author_email='sananthanatarajan12@gmail.com',
    packages=['image_scraper'],
    test_suite='tests',
    url='https://github.com/sananth12/ImageScraper/',
    description='A simple image scraper to download all images from a given url',
      )
