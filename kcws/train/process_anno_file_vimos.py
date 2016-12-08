# -*- coding: utf-8 -*-
# @Author: Vimos Tan
# @Date:   2016-12-07 18:52:40
import sys
import os
import re
import codecs

# pat1 = re.compile(ur"( ?\[.+?\].+? +|.+? +)")
pat1 = re.compile(ur'((?: ?\[.+?\])?.+? +)')
pat2 = re.compile(ur"\[(?P<words>.+?)\]")


def process_item(line):
    for item in pat1.findall(line):
        item = item.strip()
        if item.startswith('['):
            for i_item in pat2.findall(item):
                for z_item in i_item.split(' '):
                    yield z_item
        else:
            yield item


def process_line(line):
    s = []
    for item in process_item(line):
        try:
            words, _ = item.rsplit("/", 1)
            s.extend(list(words))
            if words == u'。':
                sentence = u' '.join(s)
                yield sentence
                s = []
        except:
            pass

    sentence = u' '.join(s)
    yield sentence


def process_file(cur_file):
    with codecs.open(cur_file, "r", encoding="utf8") as fp:
        for l in fp:
            for s in process_line(l):
                if s:
                    yield s


def main(argc, argv):
    if argc < 3:
        print("Usage:%s <dir> <output>" % (argv[0]))
        sys.exit(1)
    root_dir = argv[1]
    with codecs.open(argv[2], "w", encoding='utf8') as out:
        for dir_name, _, file_list in os.walk(root_dir):
            for f in filter(lambda x: x.endswith(".txt"), file_list):
                [out.write(u"{}\n".format(s)) for s in process_file(os.path.join(root_dir, dir_name, f))]


if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
