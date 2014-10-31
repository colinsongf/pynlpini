# coding=utf-8
import sys
import pynlpini.common.ascii_processor as ap
import pynlpini.common.chinese_processor as cp
from pipe import *


def normalize(txt):
    def replace_char(c):
        if c in cp.CHINESE_PUNCS + ap.ASCII_PUNCS:
            return "|"
        if c in cp.CHINESE_DIGITS + ap.ASCII_DIGITS:
            return '9'
        if c in cp.CHINESE_LOWER_LETTERS + cp.CHINESE_UPPER_LETTERS + ap.ASCII_LOWER_LETTERS + ap.ASCII_UPPER_LETTERS:
            return 'a'
        return c

    def process_token(token):
        if token.find("/") == -1:
            return ''.join(token | select(replace_char))
        else:
            tmp = token.split("/")
            if len(tmp) == 2:
                word = tmp[0]
                pos = tmp[1]
                return ''.join(word | select(replace_char)) + "/" + pos
            else:
                return token

    tokens = txt.split()
    return ' '.join(tokens | select(process_token))


def tag(raw_file_path, normalize_file_path, tag_file_path):
    with open(raw_file_path, "r") as raw_file:
        with open(normalize_file_path, "w") as normalize_file:
            for line in raw_file:
                line = line.decode("utf-8").strip()
                line = normalize(line)
                normalize_file.write(line.encode("utf-8") + "\n")

    with open(normalize_file_path, "r") as normalize_file:
        with open(tag_file_path, "w") as tag_file:
            for line in normalize_file:
                line = line.decode("utf-8").strip()
                if len(line) == 0:
                    continue
                tokens = line.split()
                for token in tokens:
                    if token.find("/") != -1:
                        tmp = token.split("/")
                        if len(tmp) != 2:
                            continue
                        word = tmp[0]
                        pos = tmp[1]
                        length = len(word)
                        if length == 1:
                            tag_file.write(word[0].encode("utf-8") + " S-" + pos.encode("utf-8") + "\n")
                        else:
                            if length > 1:
                                tag_file.write(word[0].encode("utf-8") + " B-" + pos.encode("utf-8") + "\n")
                                for i in range(1, length):
                                    tag_file.write(word[i].encode("utf-8") + " I-" + pos.encode("utf-8") + "\n")
                            else:
                                continue
                    else:
                        for i in range(1, len(token)):
                            tag_file.write(token[i].encode("utf-8") + " N" + "\n")

                tag_file.write("\n")


if __name__ == '__main__':
    tag(sys.argv[1], sys.argv[2], sys.argv[3])
