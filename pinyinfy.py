#!/usr/bin/python

import sys
import os
from cconvert import CConvert

class Pinyinfyer:

  def __init__(self):
    print "initialize converter..."
    self.path = sys.argv[1]
    self.utf8_alnum = {}
    for i in range(10):
      self.utf8_alnum[unicode(i)] = str(i)
    for c in xrange(ord('a'), ord('z')+1):
      self.utf8_alnum[unicode(chr(c))] = chr(c)
    for c in xrange(ord('A'), ord('Z')+1):
      self.utf8_alnum[unicode(chr(c))] = chr(c)
    self.utf8_alnum[u'.'] = '.'
    self.utf8_alnum[u'_'] = "-"
    self.utf8_alnum[u'-'] = "-"
    self.utf2pinyin = {}
    with open("./convert-utf-8.txt") as fp:
      for line in fp:
        utf8_line = line.strip().decode('utf-8')
        pinyin = utf8_line[1:]
        if u"," in pinyin:
          pinyin=pinyin.split(u",")[0][:-1]
        else:
          pinyin=pinyin[0:-1]
        self.utf2pinyin[utf8_line[0]] = pinyin


  def _translate_char(self, char):
    if char in self.utf2pinyin:
      return '-'+self.utf2pinyin[char]
    elif char in self.utf8_alnum:
      return self.utf8_alnum[char]
    else:
      return None

  def _translate_word(self, word):
    utf8_word = word.strip().decode('utf-8')
    utf8_word = utf8_word.replace(u" ", "")
    pinyins = []
    for char in utf8_word:
      pinyin = self._translate_char(char)
      if pinyin is not None:
        pinyins.append(pinyin)
    return "".join(pinyins).lstrip('-')

  def _change_name(self, path, original, new):
    os.rename(path+'/'+original, path+'/'+new)


  def work(self):
    visited_dirs = set()
    for root, dirs, files in os.walk(self.path):
      for name in files:
        original = name
        new  = self._translate_word(name).encode('utf-8')
        self._change_name(root,original , new)
      for name in dirs:
        if name not in visited_dirs:
          original = name
          new  = self._translate_word(name).encode('utf-8')
          self._change_name(root,original , new)
          visited_dirs.add(name)
      dir_name = root.split(os.path.sep)[-1]
      if dir_name not in visited_dirs:
        new  = self._translate_word(dir_name).encode('utf-8')
        self._change_name(root, original , new)
        visited_dirs.add(name)



if __name__ == "__main__":
  p = Pinyinfyer()
  p.work()
