#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2008, Gianluca Fiore
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

import re
import urllib2
from urllib import urlretrieve, urlencode
from cookielib import CookieJar
from os.path import join
import lxml.html
from pyimg import user_agent



# The regexp we'll need to find the link
rRedirects = re.compile("uploadimg\-streamate\.php", re.IGNORECASE) # to find the page with streamate ads
rRedirects2 = re.compile("Continue To Your Image", re.IGNORECASE) # to find generical redirects
rRedirects3 = re.compile("tempfull-default\.php", re.IGNORECASE) # to find the url of the imagevenue's countdown


values = {}
headers = { 'User-Agent' : user_agent }
data = urlencode(values)
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
urllib2.install_opener(opener)

def imagevenue_parse(link, basedir):
    """For parsing normal imagevenue's links"""

    request = urllib2.Request(link, data, headers)
    try:
        response = urllib2.urlopen(request)
        # search if the image link goes to a "Continue to image" page. 
        # If so substitute the url part with the real image one and request the page again
        redirect = re.search(rRedirects3, response.geturl())
        if redirect:
            realurl = rRedirects3.sub('img.php', response.geturl())
            try:
                response = urllib2.urlopen(realurl)
            except urllib2.HTTPError as e:
                if e.code == 404:
                    print("An image couldn't be downloaded")
                    return
            except urllib2.URLError as e:
                print(e.reason)
                return
    except urllib2.HTTPError as e:
        if e.code == 404:
            print("An image couldn't be downloaded")
            return
    except urllib2.URLError as e:
        print(e.reason)
        return

    # get every page linked from the imagevenue links
    image_page = response.read()


    # if there are ads on the page, resubmit the link to the parser
    if re.search(rRedirects, image_page):
        imagevenue_parse(link, basedir)
        return
    elif re.search(rRedirects2, image_page):
        imageveneue_parse(link)
        return

    page = lxml.html.fromstring(image_page)

    # find the src attribute which contains the real link of imagevenue's images
    src_links = page.xpath("//img[@id='thepic']")

    imagevenue_src = [li.get('src', None) for li in src_links]

    imagevenue_split = re.split('img.php\?image=', link) # remove the unneeded parts
    try:
        # make up the real image url
        download_url = str(imagevenue_split[0]) + str(imagevenue_src[0])
    except IndexError:
        # if we get an IndexError just continue (it may means that the image
        # can't be downloaded from the server or there is a host's glitch
        pass

    try:
        # generate just the filename of the image to be locally saved
        save_extension = re.split('([0-9a-zA-Z]+-[0-9]+/)?loc[0-9]{,4}/', imagevenue_src[0]) 
        savefile = join(basedir, str(save_extension[-1]))
        # finally save the image on the desidered directory
        urlretrieve(download_url, savefile) 
    except IndexError:
        return


def imagevenue_embed(link):
    """For parsing the links coming from paid host images like usercash"""

    # get every page linked from the imagevenue links
    request = urllib2.Request(link, data, headers)
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        return
    except urllib2.URLError as e:
        return

    image_page = response.read()
    page = lxml.html.fromstring(image_page)

    # find the src attribute which contains the real link of imagevenue's images
    src_links = page.xpath("//img[@id='thepic']")
    imagevenue_src = []
    for li in src_links:
        imagevenue_src.append(li.get('src', None))


        imagevenue_split = re.split('img.php\?image=', link) # remove the unneeded parts
        try:
            # make up the real image url
            download_url = str(imagevenue_split[0]) + str(imagevenue_src[0])
        except IndexError:
            # if we get an IndexError just continue (it may means that the image
            # can't be downloaded from the server or there is a host's glitch
            continue

    # generate just the filename of the image to be locally saved
    save_extension = re.split('([0-9a-zA-Z]+-[0-9]+/)?loc[0-9]{,4}/', imagevenue_src[0]) 
    savefile = basedir + str(save_extension[-1])
    # finally save the image on the desidered directory
    urlretrieve(download_url, savefile) 
