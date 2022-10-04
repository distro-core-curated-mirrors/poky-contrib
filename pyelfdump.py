#! /usr/bin/env python3

import sys
import elftools.elf.elffile

def first_tag(dynamic, type):
    try:
        return next(dynamic.iter_tags(type))
    except StopIteration:
        return None

def test():
    with open(sys.argv[1], 'rb') as f:
        elffile = elftools.elf.elffile.ELFFile(f)
        dynamic = elffile.get_section_by_name(".dynamic")
        #print(dynamic['sh_type'] == 'SHT_NOBITS':
        print(dynamic['sh_type'])
        value = first_tag(dynamic, "DT_SONAME")
        if value: value.soname

        value = first_tag(dynamic, "DT_RPATH")
        if value: value.rpath

        value = first_tag(dynamic, "DT_RUNPATH")
        if value: value.runpath

        for value in dynamic.iter_tags("DT_NEEDED"):
            value.needed

test()

#import timeit
#print(timeit.timeit("test()", number=1000, globals=globals()) / 1000)
