#!/usr/bin/python

import sys, FilePathGenerator, TextFromHtmlExtractor
from urlparse import urlparse
from TextPrettyWriter import TextPrettyWriter
from Configurator import Configurator
from optparse import OptionParser


def main(argv):
    parser = OptionParser()
    parser.add_option("-a", "--article", dest="url",
                      help="Url of the article to be processed")
    parser.add_option("-o", "--ofile", dest="outputfile",
                      help="Define the output file where the result will be stored - if not set will be defined automatically")
    parser.add_option("-c", "--config", dest="config",
                      help="config file location")
    parser.add_option("-v", "--verbose", dest="verbose",action="store_true", default=False,
                      help="Print HTML parser output to stdout")

    (options, args) = parser.parse_args(argv)
    if (len(argv) < 2):
        progName = parser.get_prog_name()
        if ".py" in progName:
            print 'Please see help : python', progName, '-h'
        else:
            print 'Please see help :', progName, '-h'
        sys.exit()

    print 'Url to process "', options.url, '"'

    if not uri_validator(options.url):
        print 'Url is not valid. Exit.'
        sys.exit(1)

    configurator = Configurator(options.config)
    config = configurator.getConfig()

    textArray = TextFromHtmlExtractor.getTextArrayFromUrl(options.url, config, options.verbose)

    fileGenerator = FilePathGenerator.FilePathGenerator(options.url)
    if (options.outputfile is not None):
        file = fileGenerator.generateProvided(options.outputfile)
    else:
        file = fileGenerator.generateByUrl('./out')

    print 'Output file is "', file.name, '"'

    with TextPrettyWriter(file, config) as prettyWriter:
        prettyWriter.write(textArray)

    print 'Work completed.'

def uri_validator(x):
    try:
        result = urlparse(x)
        return True if [result.scheme, result.netloc, result.path] else False
    except:
        return False


if __name__ == "__main__":
    main(sys.argv[1:])
