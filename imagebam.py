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
rImagebam = re.compile("href=\"?http://www\.imagebam\.com/image", re.IGNORECASE)

# Our base directory
basedir = '/mnt/documents/Maidens/Uploads/'

values = {}
user_agent = 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.0.1) Gecko/2008072610 GranParadiso/3.0.1'
headers = { 'User-Agent' : user_agent }
data = urlencode(values)


def imagebam_parse(link):
    rSrcImagebam = re.compile("http://[0-9]+\.imagebam\.com/dl\.php") # regexp for the src link
    imagebam_list = [] # the list that will contain the href tags
    imagebam_list.append(link['href'])
    for i in imagebam_list:
        # get every page linked from the imagebam links
        request = urllib2.Request(i, data, headers)
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            break
        except urllib2.URLError, e:
            break
        image_page = response.read()
        #image_page = myopener.open(i).read()
        page_soup = BeautifulSoup(image_page)
        # find the src attribute which contains the real link of imagebam's images
        src_links = page_soup.findAll('img', src=rSrcImagebam)
        imagebam_src = []
        for li in src_links:
            imagebam_src.append(li['src']) # add all the src part to a list


        imagebam_split = re.split('dl\.php\?ID=', imagebam_src[0]) # remove the unneeded parts
        download_url = imagebam_src[0]
        # generate just the filename of the image to be locally saved
        # TODO: іf the image is not a jpeg how to get the correct extension?
        savefile = basedir + str(imagebam_split[1]) + ".jpg"
        # finally save the image on the desidered directory
        urlretrieve(download_url, savefile) 

