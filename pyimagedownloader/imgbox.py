#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2008-2012, Gianluca Fiore
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
###############################################################################



__author__ = "Gianluca Fiore"
__license__ = "GPL"
__email__ = "forod.g@gmail.com"

from urllib import urlretrieve
from os.path import join
import lxml.html
import logging
import http_connector

class ImgboxParse():

    def __init__(self, link, basedir):
        self.link = link
        self.basedir = basedir
        self.connector = http_connector.Connector()
        self.logger = logging.getLogger('pyimagedownloader')

    def process_url(self, url):
        response = self.connector.reqhandler(url)

        try:
            self.page = lxml.html.fromstring(response)
        except lxml.etree.XMLSyntaxError as e:
            # most of the time we can simply ignore parsing errors
            self.logger.error("XMLSyntaxError at %s" % url)
            return

        return self.page

    def imgbox_get_image_src_and_name(self, page):
        # find the src attribute which contains the real url
        src_links = page.xpath("//div[@id='cont']/img")
        imgbox_src = [li.get('src', None) for li in src_links]

        # extract also the filename of the image
        imagename = [li.get('title', None) for li in src_links]

        return imgbox_src, imagename

    def imgbox_save_image(self, src, imagename):
        download_url = src[0]
        try:
            savefile = join(self.basedir, str(imagename[-1]))
            urlretrieve(download_url, savefile)
        except IndexError as e:
            self.logger.error("IndexError in %s" % imagename)
            pass


    def parse(self):
        self.page = self.process_url(self.link)

        self.imgbox_src, self.imagename = self.imgbox_get_image_src_and_name(self.page)

        self.imgbox_save_image(self.imgbox_src, self.imagename)
