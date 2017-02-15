import FilePathGenerator, TextFromHtmlExtractor
from TextPrettyWriter import TextPrettyWriter
from BeautifulSoup import BeautifulSoup

urls = ['https://lenta.ru/news/2017/02/11/maroder/',
        'https://russian.rt.com/world/article/358299-raketa-koreya-ssha-yaponiya-kndr-tramp']
for url in urls:
    fileGenerator = FilePathGenerator.FilePathGenerator(url)
    # file
    if not (url):
        file = fileGenerator.generateProvided('C:/Work/tensor/task1/out/fixed.txt')
    else:
        file = fileGenerator.generateByUrl('./out')

    print 'Output file is "', file.name, '"'
    textArray = TextFromHtmlExtractor.getTextArrayFromUrl(url)
    with TextPrettyWriter(file) as prettyWriter:
        prettyWriter.write(textArray)
