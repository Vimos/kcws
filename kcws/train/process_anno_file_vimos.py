# -*- coding: utf-8 -*-
# @Author: Vimos Tan
# @Date:   2016-12-07 18:52:40
import sys
import os
import re
import codecs

pat1 = re.compile(ur"( ?\[.+?\].+? +|.+? +)")
pat2 = re.compile(ur"\[(?P<first_name>.+?)\]")


def processItem(line):
    for item in pat1.findall(line):
        item = item.strip()
        if item.startswith('['):
            for iitem in pat2.findall(item):
                for zitem in iitem.split(' '):
                    yield zitem
        else:
            yield item


def processLine(line):
    s = []
    for item in processItem(line):
        try:
            token, _ = item.rsplit("/", 1)
            s.extend(list(token))
            if token == u'。':
                sentence = u' '.join(s)
                yield sentence
                s = []
        except:
            pass

    sentence = u' '.join(s)
    yield sentence


def processFile(curFile):
    with codecs.open(curFile, "r", encoding="utf8") as fp:
        for l in fp:
            for s in processLine(l):
                if s:
                    yield s


def main(argc, argv):
    if argc < 3:
        print("Usage:%s <dir> <output>" % (argv[0]))
        sys.exit(1)
    rootDir = argv[1]
    with codecs.open(argv[2], "w", encoding='utf8') as out:
        for dirName, _, fileList in os.walk(rootDir):
            for f in filter(lambda x: x.endswith(".txt"), fileList):
                [out.write(u"{}\n".format(s)) for s in processFile(os.path.join(rootDir, dirName, f))]


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
