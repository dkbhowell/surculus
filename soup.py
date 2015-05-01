from bs4 import BeautifulSoup
import requests
import urllib2

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

link_class = "l _HId"

url = 'https://www.google.com/search?q=TeslaMotors&hl=en&gl=us&authuser=0&source=lnt&tbs=cdr%3A1%2Ccd_min%3A4%2F15%2F2015%2Ccd_max%3A4%2F15%2F2015&tbm=nws'
r  = requests.get(url)
html_doc = r.text

#page = urllib2.urlopen(url)
print html_doc

soup = BeautifulSoup(html_doc)

for link in soup.find_all('a'):
    if link.has_attr("class"):
        print link["class"]
        print link["href"]
        pass

#print(soup.prettify())