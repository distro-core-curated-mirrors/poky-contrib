#! /usr/bin/env python3

import sys
from oe.parsers.elf import Elf

def find_program_segment(elf, ph_type):
    for h in elf.header.program_headers:
        if h.type == ph_type:
            return h
    return None

def find_section_header(elf, sh_type):
    for h in elf.header.section_headers:
        if h.type == sh_type:
            return h
    return None

def stripped(elf):
    for h in elf.header.section_headers:
        if h.type == Elf.ShType.progbits and h.name == ".debug_info":
            return False
    return True

def is_dynamic(elf):
    return find_program_segment(elf, Elf.PhType.interp) is not None

def dynamic_by_tag(elf, tag):
    dynamic = find_section_header(elf, Elf.ShType.dynamic)
    if not dynamic:
        return None
    
    for entry in dynamic.body.entries:
        if entry.tag_enum == tag:
            yield entry.value_str

def dynamic_by_tag_first(elf, tag):
    values = dynamic_by_tag(elf, tag)
    try:
        return next(values)
    except StopIteration:
        return None

def linkage(elf):
    dynamic = find_section_header(elf, Elf.ShType.dynsym)
    if not dynamic:
        return

    strings = None
    for h in elf.header.section_headers:
        if h.type == Elf.ShType.strtab and h.name == ".dynstr":
            strings = h
    if not strings:
        return

    for entry in dynamic.dynsym.entries:
        elf._io.seek(strings.offset + entry.name_offset)
        name = elf._io.read_bytes_term(0, False, True, True).decode(u"ASCII")
        print(name)


def main():
    with Elf.from_file(sys.argv[1]) as elf:
        def print(s):
            pass
        print("ELF binary, {} {}, for {}".format({Elf.Bits.b32: "32-bit", Elf.Bits.b64: "64-bit"}[elf.bits],
                                                {Elf.Endian.le: "little-endian", Elf.Endian.be: "big-endian"}[elf.endian],
                                                elf.header.machine.name))
        print("Stripped" if stripped(elf) else "Not stripped")
        print("Dynamically linked" if is_dynamic(elf) else "Statically linked")
        print(f"SONAME {dynamic_by_tag_first(elf, Elf.DynamicArrayTags.soname)}")
        print(f"RPATH {dynamic_by_tag_first(elf, Elf.DynamicArrayTags.rpath)}")
        print(f"RUNPATH {dynamic_by_tag_first(elf, Elf.DynamicArrayTags.runpath)}")
        print(f"NEEDED {', '.join(dynamic_by_tag(elf, Elf.DynamicArrayTags.needed))}")

def test():
    with Elf.from_file(sys.argv[1]) as elf:
        soname = dynamic_by_tag_first(elf, Elf.DynamicArrayTags.soname)
        rpath = dynamic_by_tag_first(elf, Elf.DynamicArrayTags.rpath)
        runpath = dynamic_by_tag_first(elf, Elf.DynamicArrayTags.runpath)
        needed = list(dynamic_by_tag(elf, Elf.DynamicArrayTags.needed))

import timeit
print(timeit.timeit("test()", number=1000, globals=globals()) / 1000)
