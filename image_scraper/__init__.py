
import sys
from lxml import html
import requests
import urlparse
import os

URL = raw_input("Enter URL to scrap: ")

page = requests.get(URL)

tree = html.fromstring(page.text)
img = tree.xpath('//img/@src')

if len(img)==0:
    sys.exit( "Sorry, no images found")

print "Found %s images: "%len(img)

no_to_download = int(input('How many images to you want ? : '))
images = [urlparse.urljoin(page.url, url) for url in img] 

for x  in range(0,len(img)):
    if  img[x][:4]!="http":
        img[x]="https:"+img[x]

if not os.path.exists('images'):
    os.makedirs('images')

count=0
for img_url in img :
    tmp = requests.request('get',img_url)
    f = open('images/%s' % img_url.split('/')[-1], 'w')
    f.write( tmp.content)
    f.close()
    count+=1
    if count==no_to_download:
        break
print "Done."


