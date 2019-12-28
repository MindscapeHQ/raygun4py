from raygun4py import raygunprovider
from scrapy import signals
from scrapy.exceptions import NotConfigured


class Provider(object):
    def __init__(self, api_key):
        self.sender = raygunprovider.RaygunSender(api_key)

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get("RAYGUN_API_KEY")
        if not api_key:
            raise NotConfigured

        extension = cls(api_key)
        crawler.signals.connect(extension.spider_error, signals.spider_error)
        crawler.signals.connect(extension.item_error, signals.item_error)

        return extension

    def _handle_exception(self, failure):
        self.sender.send_exception(exc_info=(failure.type, failure.value, failure.tb))

    def item_error(self, item, response, spider, failure):
        self._handle_exception(failure)

    def spider_error(self, failure, response, spider):
        self._handle_exception(failure)
