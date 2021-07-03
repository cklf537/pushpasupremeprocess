from bs4 import *
import os
import requests
from requests.api import post, request
from facebook_scraper import get_posts

def stripImagesFromSource(srcparms):
    for imageKey, image in enumerate(srcparms[0]):
        if image[0].find('/') != -1:
            try:
                postId = (image[0].split('/'))[len(image[0].split('/'))-1]
                try:
                    for post in get_posts(postId, timeout=10, credentials=[srcparms[2], srcparms[3]]):
                        postImageUrl = post['image']
                        fbImageName = postId+'_'+(((postImageUrl.split('?'))[0]).split('/'))[len(((postImageUrl.split('?'))[0]).split('/'))-1]
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        try:
                            responseContent = requests.get(postImageUrl, headers=headers).content
                            with open(f"{srcparms[4]}/{fbImageName}", "wb+") as f:
                                f.write(responseContent)
                                break
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)