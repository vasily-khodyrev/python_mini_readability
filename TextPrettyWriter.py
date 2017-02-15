"""File path generator based on the provided Url
   - Generates file path based on the provided URL
   - Creates all intermediate directories in the path

Simple usage example:

   prettyWriter = TextPrettyWriter(file, {'line_max':80})
   ...
   prettyWriter.write(text_array)
   ...
   prettyWriter.close()

   or

   with TextPrettyWriter(file) as prettyWriter:
       prettyWriter.write()

   ...and that's all - file will be closed automatically
"""
import textwrap

class TextPrettyWriter:
    def __init__(self, file, options={'MAX_LINE_LENGTH': 80}):
        self._file = file
        self._options = options

    def write(self, texts=[]):
        textwrapper = textwrap.TextWrapper(self._options.get('MAX_LINE_LENGTH', 80))
        for line in texts:
            if line in ('\n'):
                res_text = line
            else:
                res_text = textwrapper.fill(line).encode("utf-8")
            self._file.write(res_text)

    def close(self):
        self._file.close()

    def __enter__(self):
        return self

    def __exit__(self ,type, value, traceback):
        self.close()