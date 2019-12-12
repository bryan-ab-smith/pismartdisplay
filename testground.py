import urllib.request
import xml.etree.ElementTree as ET

feedReq = urllib.request.urlopen('https://www.sbs.com.au/news/feed')
feed = feedReq.read()
doc = ET.fromstring(feed)

arts = doc.findall('channel/item/title')
descs = doc.findall('channel/item/description')

print(arts[0].text)
print(descs[0].text)

print('\n')
print(arts[1].text)
print(descs[1].text)

print('\n')
print(arts[2].text)
print(descs[2].text)
