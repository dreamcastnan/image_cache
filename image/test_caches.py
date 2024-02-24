import unittest
from unittest.mock import call, Mock

from image.caches import ImageCache


class TestImageCache(unittest.TestCase):

    def setUp(self):
        # setup a mock ImageClient that returns empty bytes for every image url
        mock_image_client = Mock()
        mock_image_client.get.return_value = bytes()

        self.mock_image_client = mock_image_client

    def test_lease_returns_from_cache_when_present(self):
        image_cache = ImageCache(self.mock_image_client)
        url = "http://canva-interview.com/image.png"

        # populate the cache
        image1 = image_cache.lease(url)

        # request the same image a second time
        image2 = image_cache.lease(url)

        # ensure that each subsequent call to lease returned the same File
        # reference for the cached image
        self.assertEqual(image1, image2)
        # and that the image_client was only called once with this url
        self.mock_image_client.get.assert_called_once_with(url)

        # release the image as many times as leased to enable cleanup
        image_cache.release(url)
        image_cache.release(url)

    def test_lease_does_not_return_the_same_image_for_diff_urls(self):
        image_cache = ImageCache(self.mock_image_client)
        url1 = "http://canva-interview.com/image1.png"
        url2 = "http://canva-interview.com/image2.png"

        # fetch two different image urls
        image1 = image_cache.lease(url1)
        image2 = image_cache.lease(url2)

        # ensure that the file handles are different (images are stored in different files)
        self.assertNotEqual(image1, image2)

        # ensure that the image_client was called twice with different urls
        self.mock_image_client.get.assert_has_calls([call(url1), call(url2)])

        # release the leased images to enable cleanup
        image_cache.release(url1)
        image_cache.release(url2)

    def test_release_does_not_cleanup_actively_leased_images(self):
        image_cache = ImageCache(self.mock_image_client)
        url = "http://canva-interview.com/image1.png"

        # lease the same image twice
        image_cache.lease(url)
        image = image_cache.lease(url)

        # image should be cached on filesystem
        self.assertTrue(image.exists())

        # release image once
        image_cache.release(url)

        # image should still be cached on filesystem
        self.assertTrue(image.exists())

        # release image final time
        image_cache.release(url)

        # image should no longer exist
        self.assertFalse(image.exists())
