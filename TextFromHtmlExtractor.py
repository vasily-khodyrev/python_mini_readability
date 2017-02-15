"""
HTML <-> array of texts.

1. Can extract from HTML string
   texts = getTextArrayFromHtml(html_str)

2. Can extract text by html url
   texts = getTextArrayFromUrl(url)

"""
from HTMLParser import HTMLParser, HTMLParseError
from htmlentitydefs import name2codepoint
#from BeautifulSoup import BeautifulSoup
import re, sys, codecs
import urllib2
from urlparse import urlparse

INCLUSION_PATTERNS = [('*','itemtype','http://schema.org/NewsArticle'),
                      ('div', 'class', 'article_article-page')]

EXCLUSION_PATTERNS = [('script', None, None),
                      ('style', None, None),
                      ('aside', None, None)]

PRE_NEWLINE_SEPARATED = ['p','h1','h2','h3','h4','br']
POST_NEWLINE_SEPARATED = ['p','h1','h2','h3','h4']
ALLOW_TEXT_OUT_OF_INC_ROOTS = True
ROOT_TEXT_TAGS = ['p','h1','h2','h3','h4']

OUT = codecs.getwriter('utf-8')(sys.stdout)

class _HTMLToText(HTMLParser):
    def __init__(self, baseUrl='', config = {}, verbose = False):
        HTMLParser.__init__(self)
        self._baseUrl = baseUrl
        self._texts = []
        self._context = None
                         # tag   attrs  incl   excl   has_text
        self._tag_stack = [[None, None, False, False, False]]
        self._config = config
        self._verbose = verbose

    def __getINCLUSION_PATTERNS(self):
        return self._config.get('INCLUSION_PATTERNS',INCLUSION_PATTERNS)

    def __getEXCLUSION_PATTERNS(self):
        return self._config.get('EXCLUSION_PATTERNS', EXCLUSION_PATTERNS)

    def __getPRE_NEWLINE_SEPARATED(self):
        return self._config.get('PRE_NEWLINE_SEPARATED', PRE_NEWLINE_SEPARATED)

    def __getPOST_NEWLINE_SEPARATED(self):
        return self._config.get('POST_NEWLINE_SEPARATED', POST_NEWLINE_SEPARATED)

    def __getROOT_TEXT_TAGS(self):
        return self._config.get('ROOT_TEXT_TAGS', ROOT_TEXT_TAGS)

    def __getALLOW_TEXT_OUT_OF_INC_ROOTS(self):
        return self._config.get('ALLOW_TEXT_OUT_OF_INC_ROOTS', ALLOW_TEXT_OUT_OF_INC_ROOTS)

    def __getAttrValue(self, param):
        attrs = self._tag_stack[-1][1]
        for attr in attrs:
            if attr[0] == param:
                return attr[1]
        return None

    def __getAttrValue(self, item, param):
        attrs = item[1]
        for attr in attrs:
            if attr[0] == param:
                return attr[1]
        return None

    def __isUnderRootTextTag(self):
        if len(self._tag_stack) > 1:
            for tag_item in reversed(self._tag_stack):
                tag = tag_item[0]
                if tag is not None and tag in self.__getROOT_TEXT_TAGS():
                    return True
        return False

    def hasAttrValue(self, attrs, param, value):
        for tuple in attrs:
            if (tuple[0] == param) and (value in tuple[1]):
                return True
        return False

    def isInclusion(self):
        if len(self._tag_stack)>0:
            return self._tag_stack[-1][2]
        else:
            return False

    def isExclusion(self):
        if len(self._tag_stack) > 0:
            return self._tag_stack[-1][3]
        else:
            return False

    def __isHideOutput(self):
        return self.isExclusion() or (not self.isInclusion() and not self.__getALLOW_TEXT_OUT_OF_INC_ROOTS())

    def __closeStack(self, tag):
        '''
        Find closest open tag in stack. And removes all items in between. To solve HTML tag inconsistency issue.
        In case match tag is not found - do nothing
        :param tag: item in stack
        :return:
        '''
        ind = 0
        found = False
        for item in reversed(self._tag_stack):
            ind += 1
            if item[0] is not None and item[0] == tag:
                found = True
                break
        result = None
        if found:
            if self._verbose:
                print 'Found pair: ' + str(tag) + ' dist: ' + str(ind)
            while (ind > 0):
                result = self._tag_stack.pop()
                ind -= 1
        else:
            if self._verbose:
                print 'WARN: no pair found for end tag: ' + str(tag)

        return result


    def handle_starttag(self, tag, attrs):
        if self._verbose:
            print ' '*len(self._tag_stack) + "Start: [" + tag + "]" + str(attrs)
        isInclusion = self.isInclusion()
        for incl_filter in self.__getINCLUSION_PATTERNS():
            if (tag == incl_filter[0] or incl_filter[0] == '*') and (not incl_filter[1] or self.hasAttrValue(attrs, incl_filter[1], incl_filter[2])):
                isInclusion = True
        isExclusion = self.isExclusion()
        for excl_filter in self.__getEXCLUSION_PATTERNS():
            if (tag == excl_filter[0] or excl_filter[0] == '*') and (not excl_filter[1] or self.hasAttrValue(attrs, excl_filter[1], excl_filter[2])):
                isExclusion = True
        self._context = tag
        self._tag_stack.append([tag, attrs, isInclusion, isExclusion, False])

        if tag in self.__getPRE_NEWLINE_SEPARATED() and not self.__isHideOutput():
            self._texts.append('\n')

    def handle_endtag(self, tag):
        item = self.__closeStack(tag)
        self._context = self._tag_stack[-1][0]
        if self._verbose:
            print ' '*len(self._tag_stack) + "End: [" + tag + "]" + str(item)
        if (item is not None):
            if tag in ('a') and item[4] and not self.__isHideOutput() and self.__isUnderRootTextTag():
                link = self.__getAttrValue(item, 'href')
                if link is not None:
                    self._texts.append('[' + link + ']')
            if tag in self.__getPOST_NEWLINE_SEPARATED() and not self.__isHideOutput():
                self._texts.append('\n')

    def handle_data(self, text):
        if text:
            shortS = re.sub(r'[\s\r\n]+', ' ', text).strip()
            if len(shortS)>0:
                if self._verbose:
                    ss = u' '*len(self._tag_stack) + u'Text: [' + str(self._context) + u']' + shortS
                    OUT.write("%s\n" % ss)
                #print ' '*len(self._tag_stack) + 'Text: [' + str(self._context) + ']' + shortS
            self._tag_stack[-1][4] = True # Set textIsPresent flag
            if not self.__isHideOutput():
                if self.__isUnderRootTextTag():
                     self._texts.append(re.sub(r'[\s\r\n]+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.__isHideOutput() and self.__isUnderRootTextTag():
            c = unichr(name2codepoint[name])
            self._texts.append(c)

    def handle_charref(self, name):
        if not self.__isHideOutput() and self.__isUnderRootTextTag():
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._texts.append(unichr(n))

    def get_text_array(self):
        res = ['']
        wasNewline = False
        for text in self._texts:
            if text in '\n':
                res.append(text)
                wasNewline = True
            else:
                if not wasNewline:
                    res[-1] += text
                else:
                    res.append(text)
                wasNewline = False
        return res

def html_to_text_array(html='<html/>', baseUrl='', config = {}, verbose = False):
    """
    Given a piece of HTML, return the array of texts it contains.
    """
    parser = _HTMLToText(baseUrl, config, verbose)
    try:
        parser.feed(html)
        parser.close()
    except HTMLParseError:
        pass
    return parser.get_text_array()

def getTextArrayFromHtml(html='<html/>', baseUrl='' , config = {}):
    """
    Given a piece of HTML, return the array of texts it contains.
    """
    parser = _HTMLToText(baseUrl, config)
    try:
        parser.feed(html)
        parser.close()
    except HTMLParseError:
        pass
    return parser.get_text()


def getTextArrayFromUrl(url, config={}, verbose = False):
    o = urlparse(url)
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    if response.getcode() == 200:
        contentTypeHeader = response.headers['content-type'];
        encoding = "utf-8"
        if contentTypeHeader and "charset" in contentTypeHeader:
            encoding = response.headers['content-type'].split('charset=')[-1];
        the_page = unicode(response.read(),encoding)
        #Fix html if there're any unclosed tags
        #soup = BeautifulSoup(the_page)
        #correct_html = unicode(soup.prettify(),"utf-8")
        correct_html = the_page
        return html_to_text_array(correct_html, o.scheme + "://" + o.netloc, config, verbose)
    else:
        raise Exception('Cannot get web page by url: ' + url, 'Server response: ' + response.getcode() + ' msg: ' + response.msg())
