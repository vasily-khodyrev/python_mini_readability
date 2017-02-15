from BeautifulSoup import BeautifulSoup
import urllib2

url = 'https://www.gazeta.ru/lifestyle/style/2017/02/a_10521767.shtml'

req = urllib2.Request(url)
response = urllib2.urlopen(req)
if response.getcode() == 200:
    encoding = response.headers['content-type'].split('charset=')[-1];
    the_page = unicode(response.read(),encoding)
    print the_page
    soup = BeautifulSoup(the_page)
    print soup.prettify()
else:
    raise Exception('Cannot get web page by url: ' + url, 'Server response: ' + response.getcode() + ' msg: ' + response.msg())

