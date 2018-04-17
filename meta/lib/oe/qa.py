#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

import os, struct, mmap

class NotELFFileError(Exception):
    pass

class ELFFile:
    EI_NIDENT = 16

    EI_CLASS      = 4
    EI_DATA       = 5
    EI_VERSION    = 6
    EI_OSABI      = 7
    EI_ABIVERSION = 8

    E_MACHINE    = 0x12

    # possible values for EI_CLASS
    ELFCLASSNONE = 0
    ELFCLASS32   = 1
    ELFCLASS64   = 2

    # possible value for EI_VERSION
    EV_CURRENT   = 1

    # possible values for EI_DATA
    EI_DATA_NONE  = 0
    EI_DATA_LSB  = 1
    EI_DATA_MSB  = 2

    PT_INTERP = 3

    def my_assert(self, expectation, result):
        if not expectation == result:
            #print "'%x','%x' %s" % (ord(expectation), ord(result), self.name)
            raise NotELFFileError("%s is not an ELF" % self.name)

    def __init__(self, name):
        self.name = name
        self.objdump_output = {}
        self.data = None

    def open(self):
        with open(self.name, "rb") as f:
            try:
                self.data = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
            except ValueError:
                # This means the file is empty
                raise NotELFFileError("%s is empty" % self.name)

    def abiSize(self):
        if self.elf.bits == Elf.Bits.b32:
            return 32
        else:
            return 64

    def isLittleEndian(self):
        return self.elf.endian == Elf.Endian.le

    def isDynamic(self):
        for p in self.elf.header.program_headers:
            if p.type == Elf.PhType.interp:
                return True
        return False

    def machine(self):
        return self.elf.header.machine.value

    def symbols(self):
        for dynsym in self.elf.header.section_headers:
            if dynsym.type == Elf.ShType.dynsym:
                break
        else:
            return []

        for dynstr in self.elf.header.section_headers:
            if dynstr.type == Elf.ShType.strtab and dynstr.name == ".dynstr":
                break
        else:
            return []

        def read(entry):
            self.elf._io.seek(dynstr.offset + entry.name_offset)
            return self.elf._io.read_bytes_term(0, False, True, True).decode(u"ASCII")
        return [read(entry) for entry in dynsym.dynsym.entries]

    def run_objdump(self, cmd, d):
        import bb.process
        import sys

        if cmd in self.objdump_output:
            return self.objdump_output[cmd]

        objdump = d.getVar('OBJDUMP')

        env = os.environ.copy()
        env["LC_ALL"] = "C"
        env["PATH"] = d.getVar('PATH')

        try:
            bb.note("%s %s %s" % (objdump, cmd, self.name))
            self.objdump_output[cmd] = bb.process.run([objdump, cmd, self.name], env=env, shell=False)[0]
            return self.objdump_output[cmd]
        except Exception as e:
            bb.note("%s %s %s failed: %s" % (objdump, cmd, self.name, e))
            return ""

def elf_machine_to_string(machine):
    """
    Return the name of a given ELF e_machine field or the hex value as a string
    if it isn't recognised.
    """
    try:
        return {
            Elf.Machine.sparc.value: "SPARC",
            Elf.Machine.x86.value: "x86",
            Elf.Machine.mips.value: "MIPS",
            Elf.Machine.powerpc.value: "PowerPC",
            Elf.Machine.arm.value: "ARM",
            Elf.Machine.superh.value: "SuperH",
            Elf.Machine.ia_64.value: "IA-64",
            Elf.Machine.x86_64.value: "x86-64",
            Elf.Machine.aarch64.value: "AArch64",
            Elf.Machine.bpf.value: "BPF"
        }[machine]
    except KeyError:
        return "Unknown (%s)" % repr(machine)

def write_error(type, error, d):
    logfile = d.getVar('QA_LOGFILE')
    if logfile:
        p = d.getVar('P')
        with open(logfile, "a+") as f:
            f.write("%s: %s [%s]\n" % (p, error, type))

def handle_error(error_class, error_msg, d):
    if error_class in (d.getVar("ERROR_QA") or "").split():
        write_error(error_class, error_msg, d)
        bb.error("QA Issue: %s [%s]" % (error_msg, error_class))
        d.setVar("QA_ERRORS_FOUND", "True")
        return False
    elif error_class in (d.getVar("WARN_QA") or "").split():
        write_error(error_class, error_msg, d)
        bb.warn("QA Issue: %s [%s]" % (error_msg, error_class))
    else:
        bb.note("QA Issue: %s [%s]" % (error_msg, error_class))
    return True

def add_message(messages, section, new_msg):
    if section not in messages:
        messages[section] = new_msg
    else:
        messages[section] = messages[section] + "\n" + new_msg

def exit_with_message_if_errors(message, d):
    qa_fatal_errors = bb.utils.to_boolean(d.getVar("QA_ERRORS_FOUND"), False)
    if qa_fatal_errors:
        bb.fatal(message)

def exit_if_errors(d):
    exit_with_message_if_errors("Fatal QA errors were found, failing task.", d)

if __name__ == "__main__":
    import sys

    with ELFFile(sys.argv[1]) as elf:
        elf.open()
        print(elf.isDynamic())
