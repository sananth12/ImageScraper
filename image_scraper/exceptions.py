class DirectoryAccessError(Exception):
    pass


class DirectoryCreateError(Exception):
    pass


class ImageDownloadError(Exception):
    status_code = 0

    def __init__(self, status_code=0):
        self.status_code = status_code


class ImageSizeError(Exception):
    image_size = 0

    def __init__(self, image_size):
        self.image_size = image_size

class PageErrorException(Exception):
    status_code = 0

    def __init__(self, status_code):
        self.status_code = status_code
