import argparse
from pathlib import Path

from fw.elf import Elf, Ehdr, Phdr

parser = argparse.ArgumentParser(description="""
    Create ELF file from a given binary
""")
parser.add_argument('binary', type=argparse.FileType('rb'), help="Source file")
parser.add_argument('addr', type=str, help="LOAD address and entry point")
parser.add_argument('elf', type=argparse.FileType('wb'), help="ELF image to create")
args = parser.parse_args()

ehdr = Ehdr(b'\x7fELF', Ehdr.CLASS64, 1, 1, 0, 0, 2, 0xB7, 1, int(args.addr, 16))
ehdr.e_phoff = 64
ehdr.e_ehsize = 64
ehdr.e_phentsize = 56
ehdr.e_shentsize = 64
with args.binary:
    data = args.binary.read()

phdr = Phdr(1, 0x1000, int(args.addr, 16), int(args.addr, 16), len(data), len(data), 0x5, 0x1000)
phdr.data = data

elf = Elf(ehdr, [phdr])
elf.update()
with args.elf:
    elf.save(args.elf)
