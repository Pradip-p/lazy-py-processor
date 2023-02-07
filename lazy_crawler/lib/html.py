"""
Will contain helper functions to help with html DOM

"""
from scrapy.utils.response import open_in_browser
from scrapy.selector import Selector


def to_browser(content=None, wait=True, is_text=False):
    """
    It will load the response in browser and by default wait for user to press enter
    :param content: scrapy response
    :param wait: (boolean)
    :return:
    """
    assert content is not None, "content is missing."
    open_in_browser(content)

    if wait:
        input("Press Enter to continue")
