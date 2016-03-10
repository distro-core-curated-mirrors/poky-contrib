import os,sys,re


def read_file(fl):
    with open(fl,'r') as f:
        lines = f.read().splitlines()
    return lines

def write_file(fl, content, append=''):
    if append:
        flag = 'a'
    else:
        flag = 'w'
    with open(fl, flag) as f:
        if type(content) is list:
            for line in content:
                line += os.linesep
                f.write(line)
        else:
            content += os.linesep
            f.write(content)

