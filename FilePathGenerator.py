"""File path generator based on the provided Url
   - Generates file path based on the provided URL
   - Creates all intermediate directories in the path

Simple usage example:

   from optparse import OptionParser

   fileGenerator = FileGeneratorByUrl(url)
   file = fileGenerator.generate('./out')
   file.write('File output\n')
"""
import os,re
from urlparse import urlparse

class FilePathGenerator:
    def __init__(self, url):
        self._url = url

    def generateByUrl(self, baseDir):
        o = urlparse(self._url)
        newPath = o.path
        if (newPath.endswith("/")):
            newPath = newPath + "index.txt"
        newPath = re.sub("(\.html|\.htm)$", '.txt', newPath)
        if not (newPath.endswith(".txt")):
            newPath += ".txt"
        curWD = ''
        if not (os.path.isabs(baseDir)):
            curWD = os.getcwd()
        path = os.path.join(curWD, baseDir + '/' + o.netloc + newPath)
        ensure_dir(path)
        f = open(path, 'w')
        return f

    def generateProvided(self, filePath):
        absPath = os.path.abspath(filePath)
        ensure_dir(absPath)
        f = open(absPath, 'w')
        return f



def ensure_dir(filePath):
    d = os.path.dirname(filePath)
    if not os.path.exists(d):
        os.makedirs(d)