#!/usr/bin/python
import sys

def read_mapper_input(stdin):
    for line in stdin:
        yield line.rstrip()

def main():
    for line in read_mapper_input(sys.stdin):
        docid = line.split('|')[0]
        document = line.split('|')[1]
        frequencies = {}
        for word in document.split():
            try:
                frequencies[word] += 1
            except KeyError:
                frequencies[word] = 1
        for word in frequencies:
            print '%s\t%s\t%s' % (word, docid, frequencies[word])
if __name__ == "__main__":
    main()
