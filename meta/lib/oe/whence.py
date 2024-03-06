#! /usr/bin/env python3

import sys
import re
import dataclasses

@dataclasses.dataclass()
class Driver:
    name: str
    description: str
    files: list[str] = dataclasses.field(default_factory=list)
    licence_name: str = None
    licence_file: str = None

def prime(fn):
    def wrapper(*args, **kwargs):
        v = fn(*args, **kwargs)
        v.send(None)
        return v
    return wrapper

class Parser:
    def __init__(self):
        self.state_new_device = self.parse_new_device()
        self.state_files = self.parse_files()
        self.state_licence = self.parse_licence()
        self.state = self.state_new_device

        self.driver = None
        self.drivers = {}

    def send(self, line):
        try:
            self.state.send(line)
        except StopIteration:
            self.stopped = True

    @prime
    def parse_new_device(self):
        while True:
            line = yield
            m = re.match(r"Driver: *(?P<name>\S*)[ -]*(?P<description>.+)?", line)
            if m:
                name, description = m.groups()
                try:
                    self.driver = self.drivers[name]
                except KeyError:
                    self.driver = Driver(name, description)
                    self.drivers[name] = self.driver
                self.state = self.state_files

    @prime
    def parse_files(self):
        while True:
            line = yield
            if line.startswith("------"):
                self.state = self.state_new_device
                continue

            m = re.match(r"(?:RawFile|File):\s*(.+)", line)
            if m:
                # TODO: also need to handle escapes?
                self.driver.files.append(m.group(1).strip('"'))
                continue

            m = re.match(r"Link:\s*(.+)", line)
            if m:
                linkname, target = m.group(1).split("->")
                linkname = linkname.strip().replace(r"\ ", " ")
                self.driver.files.append(linkname)
                continue

            m = re.match(r"Licen[cs]e:", line)
            if m:
                self.state = self.state_licence
                self.state.send(line)
                continue

    @prime
    def parse_licence(self):
        while True:
            line = yield
            if line.startswith("------"):
                self.state = self.state_new_device
                continue

            m = re.match(r"Licen[cs]e: *Redistributable.*(LICEN[CS]E\.(\S+?)(?:\.txt)?) for details", line)
            if m:
                self.driver.licence_name = m.group(2)
                self.driver.licence_file = m.group(1)
                self.state = self.state_files
                continue

            # TODO handle inline

            # fails to handle multiple license texts, such as
            # Licence: Redistributable. See LICENCE.xc5000 and LICENCE.xc5000c for details
            # or
            # License: Redistributable. See LICENSE.ice for details
            # License: Redistributable. See LICENSE.ice_enhanced for details

    def parse(self, filename):
        with open(filename) as f:
            for line in f:
                self.send(line.strip())
    
        return self.drivers.values()

if __name__ == "__main__":
    parser = Parser()

    drivers = parser.parse(sys.argv[1])

    print(f"Parsed {len(drivers)} drivers")
    for d in drivers:
        print(f"{d.name} ({d.description})")
        print(d.files)
        print(d.licence_file)
