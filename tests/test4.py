import WebArticleParserCLI

urls = ['http://lenta.ru/news/2013/03/dtp/index.html',
'https://lenta.ru/news/2017/02/11/maroder/',
'https://lenta.ru/news/2017/02/10/polygon/',
'https://russian.rt.com/world/article/358299-raketa-koreya-ssha-yaponiya-kndr-tramp',
'https://russian.rt.com/russia/news/358337-sk-proverka-gibel-devochki',
'https://www.gazeta.ru/lifestyle/style/2017/02/a_10521767.shtml',
'http://www.vedomosti.ru/realty/articles/2017/02/11/677217-moskva-zarabotala-na-parkovkah']


for url in urls:
    argv = ['-a', url, '-c', './../webarticleparser.ini', '-v']
    WebArticleParserCLI.main(argv)

#argv = ['-a','https://www.gazeta.ru/lifestyle/style/2017/02/a_10521767.shtml', '-c', './../webarticleparser.ini']
#WebArticleParserCLI.main(argv)