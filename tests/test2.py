import FilePathGenerator
from TextPrettyWriter import TextPrettyWriter
import os

url= 'https://lenta.ru/news/2017/02/11/maroder/'

texts = ['This is short text',
         '\n',
         'This is long 1 long 2 long 3 . This is long 4 long 5 long 6 . This is long 7 long 8 long 9.',
         '\n',
         'The end']
fileGenerator = FilePathGenerator.FilePathGenerator(url)
file = fileGenerator.generateProvided('C:/Work/tensor/task1/out/fixed.txt')
print 'Output file is "', file.name, '"'

with TextPrettyWriter(file) as prettyWriter:
    prettyWriter.write(texts)

