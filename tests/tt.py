import sys, codecs, locale
print sys.stdin.encoding
sys.stdin = codecs.getreader(locale.getpreferredencoding())(sys.stdin)
line = sys.stdin.readline(); 
print type(line), len(line)