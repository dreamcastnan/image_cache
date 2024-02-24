from pathlib import Path
import image.files as files
import uuid


class ImageCacheException(Exception):
    def __init__(self, message: str):
        self.message = message


class ImageCache:
    """
    Caches images on the filesystem.

    It should abide to the following contract:
       * If an image doesn't exist in the cache, it will be downloaded and
         added when first leased (through ImageCache.lease).
       * Downloading an image or returning one from the cache should be
         transparent to the caller. i.e. Leasing an image (through
         ImageCache.lease) will return a Path reference to an image,
         regardless of its presence in the cache before the call to
         ImageCache.lease.
       * An image will exist in the cache until all leases have been released
         (through ImageCache.release)
    """
    def __init__(self, image_client):
        # key: url, value: (count, fileLocation)
        self.cache = dict()
        self.imageClient = image_client
        # self.folder = Path("temp")
        # self.folder.parent.mkdir(parents=True, exist_ok=True)

        pass

    def lease(self, url: str) -> Path:
        """
        Downloads an image represented by a url or returns a previously
        downloaded image. Regardless, until a leased image is released, the
        file should exist on the file system for other processes to access.

        Args:
            url: The url of the image to download.

        Returns:
            A reference to the location on disk which this image can be accessed at.

        Raises:
            ImageCacheException: An error occurred when leasing
        """
        if not url:
            raise("invalid input")
        
        if url not in self.cache:
            image = self.imageClient.get(url)
            uName = str(uuid.uuid4())
            filepath = Path("temp/" + uName)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            files.write(filepath, image)
            self.cache[url] = [1, filepath]
        else:
            self.cache[url][0] += 1
        
        return self.cache[url][1]


    def release(self, url: str):
        """
        Releases an image from the cache. After an image is released by all
        processes leasing it, then it is no longer safe for another process to
        access the referenced image file because it will have been deleted.

        Args:
            url: the original url of the image that was leased.

        Raises:
            ImageCacheException: An error occurred when releasing
        """
        if url in self.cache:
            self.cache[url][0] -= 1
            if self.cache[url][0] == 0:
                # delete file
                filepath = self.cache[url][1]
                files.delete(filepath)
                del self.cache[url]
        else:
            return

