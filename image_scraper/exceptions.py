""" Contains all the custom exceptions used. """

class DirectoryAccessError(Exception):
    """ Exception to be raised when the directory can't be accessed. """
    pass


class DirectoryCreateError(Exception):
    """ Exception to be raised when the directory can't be created. """
    pass


class ImageDownloadError(Exception):
    """ Exception to be raised when the imace can't be downloaded. """
    status_code = 0

    def __init__(self, status_code=0):
        super(ImageDownloadError, self).__init__()
        self.status_code = status_code


class ImageSizeError(Exception):
    """ Exception to be raised when the image is over the file size. """
    image_size = 0

    def __init__(self, image_size):
        super(ImageSizeError, self).__init__()
        self.image_size = image_size


class PageLoadError(Exception):
    """ Exception to be raised when the page can't be loaded. """
    status_code = 0

    def __init__(self, status_code):
        super(PageLoadError, self).__init__()
        self.status_code = status_code
