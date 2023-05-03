import unittest

from unittest.mock import MagicMock, call
from twisted.python import failure
from raygun4py.extension.scrapy import Provider
from scrapy.http import Response
from scrapy.spiders import Spider
from scrapy.utils.test import get_crawler
from scrapy.item import Item
from scrapy.signals import item_error, spider_error
from scrapy.exceptions import NotConfigured


class TestProvider(unittest.TestCase):
    def _getDivisionFailure(self):
        try:
            1 / 0
        except:
            f = failure.Failure()
        return f

    def test__handler_exception_called(self):
        provider = Provider(api_key="test")
        crawler = get_crawler(Spider)
        spider = crawler._create_spider("scrapytest.org")
        item = Item()
        response = Response("scrapytest.org", status=400)

        provider._handle_exception = MagicMock()
        failure = self._getDivisionFailure()

        provider.item_error(item, response, spider, failure)

        provider._handle_exception.assert_called_once_with(failure)

    def test_from_crawler_not_configured(self):
        crawler = get_crawler(Spider, settings_dict=None)
        self.assertRaises(NotConfigured, Provider.from_crawler, crawler)

    def test_from_crawler_configured(self):
        crawler = get_crawler(Spider, settings_dict={"RAYGUN_API_KEY": "test"})
        crawler.signals.connect = MagicMock()
        provider = Provider.from_crawler(crawler)

        crawler.signals.connect.assert_has_calls(
            [
                call(provider.spider_error, spider_error,),
                call(provider.item_error, item_error,),
            ],
            any_order=True,
        )