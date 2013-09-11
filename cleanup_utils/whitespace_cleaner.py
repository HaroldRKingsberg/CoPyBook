'''
Created on Sep 9, 2013

@author: Harold
'''
import os

dirs = [
    'C:\\Users\\Harold\\workspace\\CoPyBook\\src\\main\\',
    'C:\\Users\\Harold\\workspace\\CoPyBook\\src\\test\\'
]

if __name__ == '__main__':
    paths = [d + ender for d in dirs for ender in os.listdir(d) if ender.endswith('.py')]
    for path in paths:
        with open(path, 'r') as f:
            content = '\n'.join(line.rstrip() for line in f)
        with open(path, 'w') as f:
            f.write(content)