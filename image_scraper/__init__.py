
import sys
from lxml import html
import requests
import urlparse
import os
from progressbar import *

def process_links(links):
    x=[]
    for l in links:
        if(l[-3:]=="jpg" or l[-3:]=="png" or l[-3:]=="gif"):
                x.append(l)
    return x
 
URL = raw_input("Enter URL to scrap: ")

page = requests.get(URL)

tree = html.fromstring(page.text)
#img = tree.xpath('//img/@src')
img = tree.xpath('//img/@src')

links = tree.xpath('//a/@href')

img_links =  process_links(links)

##sub_img = tree.xpath('//descendant-or-self::*[img]/img/@src') 

img.extend(img_links)

if len(img)==0:
    sys.exit( "Sorry, no images found")

print "Found %s images: "%len(img)

no_to_download = int(input('How many images do you want ? : '))

images = [urlparse.urljoin(page.url, url) for url in img] 

for x  in range(0,len(img)):
    if  img[x][:4]!="http":
        img[x]="https:"+img[x]

if not os.path.exists('images'):
    os.makedirs('images')

count=0
bar="["
percent=0.0
failed=0
widgets = ['Progress: ', Percentage(), ' ', Bar(marker=RotatingMarker()),' ', ETA(), ' ', FileTransferSpeed()]
pbar = ProgressBar(widgets=widgets, maxval=100).start()


for img_url in img :
    try:
    	tmp = requests.request('get',img_url)
    	f = open('images/%s' % img_url.split('/')[-1], 'w')
    	f.write( tmp.content)
    	f.close()    
	count+=1
        percent = percent + 100.0/len(img)
        pbar.update( percent )
    
    except:
        failed +=1
	#print "Can't download %s"%img_url
    if count==no_to_download:
        	break

pbar.finish()
print 
print "Done. Failed to download %s images"%failed


	
