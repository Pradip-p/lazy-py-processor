import asyncio
from pyppeteer import launch

import asyncio
from pyppeteer import launch
from typing import List


async def main(url: str, headless: bool, proxy: str = None, cookies: List[dict] = None, useragent: str = None,
               headers: dict = None, timeout: int = 0, close: bool = True):
    """
    :param useragent:
    :param timeout: int
    :param headers: dict
    :param  url: str
    :param headless: bool
    :param proxy: proxy (<proxy_type>://<username>:<password>@<host}>:<port>)
    :param cookies: List[dict]
                    Each dictionary in cookie expects from these fields
                    name (str): required
                    value (str): required
                    url (str)
                    domain (str)
                    path (str)
                    expires (number): Unix time in seconds
                    httpOnly (bool)
                    secure (bool)
                    sameSite (str): 'Strict' or 'Lax'

    :return: Dict[cookies,content,response_headers]
    """
    options = {}
    # timeout = 0
    if timeout:
        timeout = 0
    if headless:
        options['headless'] = True
    else:
        options['headless'] = False
    if proxy:
        proxy = proxy.split('//')[-1]
        options['args'] = ['--proxy-server={}'.format(proxy.split('@')[1])]
    browser = await launch(options)
    page = await browser.newPage()
    if headers:
        await page.setExtraHTTPHeaders(headers)
    if useragent:
        await page.setUserAgent(useragent)
    if proxy:
        await page.authenticate(
            {'username': proxy.split('@')[0].split(':')[0], 'password': proxy.split('@')[0].split(':')[1]})
    if cookies:
        await page.setCookie(*cookies)
    print('visiting url', url)
    try:
        response = await page.goto(url, timeout=timeout)
    except TimeoutError:
        print('Timeout')

    if not close:
        return {'page': page, 'response': response}
    print('page loaded')
    cookies = await page.cookies()
    # print('cookies', cookies)
    content = await page.content()
    # print(await browser.userAgent())
    response_headers = response.headers
    await browser.close()
    print(response.request.headers)
    return {'response_headers': response_headers, 'cookies': cookies, 'content': content}


def browse(url: str, headless: bool = True, proxy: str = None, cookies: list = None, useragent: str = None,
           headers: dict = None, timeout: int = 0, close: bool = True): 

            data = asyncio.get_event_loop().run_until_complete(main(url=url, headless=headless, proxy=proxy, cookies=cookies, useragent=useragent, headers=headers,
            timeout=timeout, close=close))
            return data

