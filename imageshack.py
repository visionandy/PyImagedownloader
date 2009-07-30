#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
"""
"""
###############################################################################



__author__ = "Gianluca Fiore"
__license__ = "GPL"
__email__ = "forod.g@gmail.com"

import re
import urllib2
from urllib import urlencode, urlretrieve
from BeautifulSoup import BeautifulSoup, SoupStrainer




# The regexp we'll need to find the link
rJpgSrc = re.compile('.(jpg|png|gif|jpeg)', re.IGNORECASE) # generic src attributes regexp
rImageshack = re.compile("href=\"?http://img[0-9]{,3}\.imageshack\.us", re.IGNORECASE)

# Our base directory
basedir = '/mnt/documents/Maidens/Uploads/'

values = {}
user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.1) Gecko/2008072610 GranParadiso/3.0.1'
headers = { 'User-Agent' : user_agent }
data = urlencode(values)

def imageshack_parse(link):
    rSrcImageshack = re.compile('/img[0-9]+/[0-9]+/[a-zA-Z0-9]+\.[jpg|gif|png]', re.IGNORECASE)
    imageshack_list = [] # the list that will contain the href tags
    imageshack_list.append(link['href'])
    for i in imageshack_list:
        request = urllib2.Request(i, data, headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            break
        except urllib2.URLError as e:
            break
        # get every page linked from the imageshack links
        image_page = response.read()
        page_soup = BeautifulSoup(image_page)
        # find the src attribute which contains the real link of imageshack's images
        src_links = page_soup.findAll('img', src=rSrcImageshack)
        #src_links = page_soup.findAll('link', rel='image_src')
        imageshack_src = []
        for li in src_links:
            imageshack_src.append(li['src']) # add all the src part to a list

        try:
            # generate just the filename of the image to be locally saved
            save_extension = re.split('img[0-9]{,3}/[0-9]+/', imageshack_src[0])
            # extract just the first part of the url to join with imageshack_src
            url_extension = re.split('/i/', i)

            savefile = basedir + str(save_extension[1])
            download_url = url_extension[0] + imageshack_src[0]
            # finally save the image on the desidered directory
            urlretrieve(download_url, savefile) 
        except IndexError:
            break
