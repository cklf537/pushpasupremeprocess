from bs4 import *
import os
import requests
from requests.api import post, request
from facebook_scraper import get_posts

def stripImagesFromSource(imageObject):
    for imageKey, image in enumerate(imageObject[0]):
        if image[0].find('/') != -1:
            try:
                postId = (image[0].split('/'))[len(image[0].split('/'))-1]
                try:
                    for post in get_posts(postId, timeout=10, credentials=['username', 'password']):
                        postImageUrl = post['image']
                        fbImageName = postId+'_'+(((postImageUrl.split('?'))[0]).split('/'))[len(((postImageUrl.split('?'))[0]).split('/'))-1]
                        headers = {'User-Agent': 'Mozilla/5.0'}
                        try:
                            responseContent = requests.get(postImageUrl, headers=headers).content
                            with open(f"/path/{fbImageName}", "wb+") as f:
                                f.write(responseContent)
                                break
                        except Exception as e:
                            print(e)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)



    
    # for post in get_posts('2016205291964907'):
    #     postImageUrl = post['image']
    #     headers = {'User-Agent': 'Mozilla/5.0'}
    #     r = requests.get(postImageUrl, headers=headers).content
    #     with open(f"/home/shekar/Documents/Python/photos/poto/1.jpeg", "wb+") as f:
    #         f.write(r)
    #     print(post['text'][:50])
