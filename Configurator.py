"""Read the config file and returns a dict with all the needed paramaters for HTML parsing and formatting
   If file is not present or some params are missing - returns default configuration

Sample config file:
[General]
root_text_tags = p:h1:h2:h3:h4

[Inclusion]
inclusion_pattern1 = div:itemtype:http://schema.org/NewsArticle
inclusion_pattern2 = div:class:article_article-page

[Exclusion]
exclusion_patterns1 = script::
exclusion_patterns2 = style::

[Format]
max_line_length=80
pre_newline_separated = p:h1:h2:h3:h4:br
post_newline_separated = p:h1:h2:h3:h4

Simple usage example #1:
   configurator = Configurator('webarticleparse.ini')
   options = configurator.getConfig()

   print options.MAX_LINE_LENGTH

Simple usage example #2:
   configurator = Configurator()
   options = configurator.getConfig()

   print options.MAX_LINE_LENGTH
"""
import os, ConfigParser

DEFAULT_INCLUSION_PATTERNS = [('div', 'itemtype', 'http://schema.org/NewsArticle'),
                              ('div', 'class', 'article_article-page')]

DEFAULT_EXCLUSION_PATTERNS = [('script', None, None),
                              ('style', None, None)]

DEFAULT_PRE_NEWLINE_SEPARATED = ['p', 'h1', 'h2', 'h3', 'h4', 'br']
DEFAULT_POST_NEWLINE_SEPARATED = ['p', 'h1', 'h2', 'h3', 'h4']

DEFAULT_ROOT_TEXT_TAGS = ['p', 'h1', 'h2', 'h3', 'h4']
DEFAULT_ALLOW_TEXT_OUT_OF_INC_ROOTS = False
DEFAULT_MAX_LINE_LENGTH = 80


class Configurator:
    def __init__(self, configPath=''):
        self._configPath = configPath

    def getConfig(self):
        '''
        Returns dictionary with parameters for HTML reader and formatter.
         If some values are absent in configuration file - defaults ones are provided.

        :return: dict with parameters read from config file
        '''
        if not self._configPath or not os.path.isfile(self._configPath):
            print 'WARN: Config file not found. Use default settings.'
            return self.getDefauls()

        config = ConfigParser.ConfigParser()
        config.read(self._configPath)

        options = self.getDefauls()
        if config.has_option('General', 'max_line_length'):
            max_line_length = config.getint('General', 'max_line_length')
            if max_line_length:
                options['MAX_LINE_LENGTH'] = max_line_length

        if config.has_option('General', 'allow_text_out_of_inclusion_roots'):
            allow_text_out_of_inclusion_roots = config.getboolean('General', 'allow_text_out_of_inclusion_roots')
            if allow_text_out_of_inclusion_roots:
                options['ALLOW_TEXT_OUT_OF_INC_ROOTS'] = allow_text_out_of_inclusion_roots

        if config.has_option('General', 'root_text_tags'):
            root_text_tags = config.get('General', 'root_text_tags')
            if root_text_tags:
                options['ROOT_TEXT_TAGS'] = root_text_tags

        if config.has_option('General', 'pre_newline_separated'):
            pre_newline_separated = config.get('General', 'pre_newline_separated')
            if pre_newline_separated:
                pre_newline_separated_list = pre_newline_separated.split(":")
                options['PRE_NEWLINE_SEPARATED'] = pre_newline_separated_list

        if config.has_option('General', 'post_newline_separated'):
            post_newline_separated = config.get('General', 'post_newline_separated')
            if post_newline_separated:
                post_newline_separated_list = post_newline_separated.split(":")
                options['POST_NEWLINE_SEPARATED'] = post_newline_separated_list

        if config.has_section('Inclusion'):
            inc_patterns = []
            inc_items = config.items('Inclusion')
            for inc_item in inc_items:
                if len(inc_item) == 2:
                    if inc_item[1]:
                        inc_item_split = inc_item[1].split(':',2)
                        if len(inc_item_split) == 3:
                            inc_patterns.append((inc_item_split[0], inc_item_split[1], inc_item_split[2]))
                        else:
                            raise Exception('Wrong format for param.', inc_item[0],
                                            ' Syntax <tag_name>:<attr_name>:<contains_value> expected')
            if len(inc_patterns)>0:
                options['INCLUSION_PATTERNS'] = inc_patterns

        if config.has_section('Exclusion'):
            exc_patterns = []
            exc_items = config.items('Exclusion')
            for exc_item in exc_items:
                if len(exc_item) == 2:
                    if exc_item[1]:
                        exc_item_split = exc_item[1].split(':',2)
                        if len(exc_item_split) == 3:
                            exc_patterns.append((exc_item_split[0], exc_item_split[1], exc_item_split[2]))
                        else:
                            raise Exception('Wrong format for param.', exc_item[0],
                                            'Syntax <tag_name>:<attr_name>:<contains_value> expected')
            if len(exc_patterns)>0:
                options['EXCLUSION_PATTERNS'] = exc_patterns

        return options

    def getDefauls(self):
        '''
        Returns default config parameters for HTML parser and formatter

        :return: dict with set of default params
        '''
        params = {'INCLUSION_PATTERNS': [],
                  'EXCLUSION_PATTERNS': [],
                  'PRE_NEWLINE_SEPARATED': [],
                  'POST_NEWLINE_SEPARATED': [],
                  'ROOT_TEXT_TAGS': [],
                  'ALLOW_TEXT_OUT_OF_INC_ROOTS': False,
                  'MAX_LINE_LENGTH': 80
                  }
        params['INCLUSION_PATTERNS'] = DEFAULT_INCLUSION_PATTERNS
        params['EXCLUSION_PATTERNS'] = DEFAULT_EXCLUSION_PATTERNS
        params['PRE_NEWLINE_SEPARATED'] = DEFAULT_PRE_NEWLINE_SEPARATED
        params['POST_NEWLINE_SEPARATED'] = DEFAULT_POST_NEWLINE_SEPARATED
        params['ROOT_TEXT_TAGS'] = DEFAULT_ROOT_TEXT_TAGS
        params['ALLOW_TEXT_OUT_OF_INC_ROOTS'] = DEFAULT_ALLOW_TEXT_OUT_OF_INC_ROOTS
        params['MAX_LINE_LENGTH'] = DEFAULT_MAX_LINE_LENGTH
        return params
