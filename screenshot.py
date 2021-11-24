#!/usr/bin/env python

# -*- coding: UTF-8 -*-

"""
@Project ：webpage-screenshot
@File ：screenshot.py
@Author ：joker
@Date ：2021/11/24 11:51
@Description: Take a screenshot of a web page using selnium. use Python3.8
"""
import os
import sys
import time
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui

print(os.getcwd())

out_dir = '%s/out' % os.getcwd()
html_filename = 'index.html'
html_save_path = '%s/%s' % (out_dir, html_filename)


def download_html_of_webpage(url):
    """
    Download html of a web page using selnium
    :param url: Url of web page
    :return: str of html
    """
    download_options = Options()
    download_options.add_argument('--headless')

    browser = webdriver.Chrome(options=download_options)
    try:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        browser.get(url)
        fw = open(html_save_path, 'w', encoding='utf-8')
        page_src = str(browser.page_source)

        print("%s page size: %d KB" % (url, sys.getsizeof(page_src) / 1024))
        fw.write(page_src)
        fw.close()
    except:
        traceback.print_exc()
        pass
    finally:
        browser.close()


def render_screenshots_locally():
    """
    Render html screenshots locally
    :return:
    """
    if not os.path.exists(html_save_path):
        return
    option = Options()
    option.add_argument('--no-sandbox')
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument("--disable-blink-features=AutomationControlled")

    browser = webdriver.Chrome(options=option)
    ele_id = 'a-page'
    try:
        # Scan the page load condition once in 5ms in 10 seconds
        wait = ui.WebDriverWait(browser, 60)
        browser.get('file://%s' % html_save_path)

        # Wait until the specified label is loaded
        wait.until(lambda driver: browser.find_element_by_id(ele_id))

        # accept cookie
        cookie_accept = browser.find_element_by_id('sp-cc-accept')
        if cookie_accept is not None:
            cookie_accept.click()

        browser.set_window_size(1080, 980)
        image_path = '%s/swebpage_screenshot.png' % out_dir
        browser.save_screenshot(image_path)
        if os.path.isfile(image_path):
            print("Successfully capture webpage screenshot")
    except:
        traceback.print_exc()
        pass
    finally:
        browser.close()


if __name__ == '__main__':
    url = 'http://www.amazon.es/gp/product/B07NR6PQ6J'

    # 1. download html
    download_html_of_webpage(url)

    # take a screenshot
    render_screenshots_locally()
