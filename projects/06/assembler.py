import argparse
import constants as C
import os
import sys


class SymbolTable(object):
    def __init__(self):
        self.table = {
            'SP': 0,'LCL':1,'ARG':2,'THIS':3, 'THAT':4, 'SCREEN':16384, 'KBD':24576, 
            'R0': 0,'R1': 1,'R2': 2,'R3': 3,'R4': 4,'R5': 5,'R6': 6,'R7': 7,'R8': 8,
            'R9': 9,'R10': 10,'R11': 11,'R12': 12,'R13': 13,'R14': 14,'R15': 15
        }
        self.c = 16

    def check(self, symbol):
        if symbol not in self.table.keys():
            self.table[symbol] = self.c
            self.c += 1
        return str(self.table[symbol])

    def set(self, symbol, line):
        self.table[symbol] = line

class HackAssembler(object):
    def __init__(self, input_fp):
        self.input_fp = input_fp
        self.table = SymbolTable()

    def setup(self):
        assert(self.input_fp[-4:] == ".asm")
        self.output_fp = self.input_fp[:-4] + ".hack"
        if os.path.exists(self.output_fp):
            sys.exit("Output file already exists")
        
        print(f'Input: {self.input_fp}')
        print(f'Ouput: {self.output_fp}')

        self.lines = list()
        lines = [line.rstrip('\n').split('//')[0].strip() for line in open(self.input_fp)]
        for line in lines:
            if line != '':
                self.lines.append(line)
        

    def replace_symbols(self):
        loop1_lines = list()
        filtered_lines = list()
        counter = 0
        for line in self.lines: 
            if line.startswith('('):
                _ = self.table.set(line.strip('()'), counter) 
            else:
                loop1_lines.append(line)
                counter += 1
        
        for line in loop1_lines:
            if line.startswith('@'):
                l = line.strip('@')
                if l.isnumeric():
                    filtered_lines.append(line)
                else:
                    filtered_lines.append('@' + self.table.check(l))
            else:
                filtered_lines.append(line) 
        self.filtered_lines = filtered_lines

    def code(self):
        self.binary_lines = list()
        for line in self.filtered_lines:
            if line[0] == '@':
                b_line = self._typeA_code(line)
            else:
                b_line = self._typeC_code(line)
            self.binary_lines.append(b_line)


    def write(self):
        with open(self.output_fp, 'a') as f:
            for line in self.binary_lines:
                # print(line)
                f.write(line + '\n')
 

    def _typeA_code(self, line):
        return format(int(line[1:]), 'b').zfill(16)
        
    
    def _typeC_code(self, line):
        comp = self._get_comp(line)
        dest = self._get_dest(line)
        jmp = self._get_jmp(line)
        return "111" + comp + dest + jmp

    
    @staticmethod
    def _get_dest(line):
        if "=" in line:
            s = line.split("=")[0]
            return str(int('A' in s)) + str(int('D' in s)) + str(int('M' in s))
        else:
            return "000" 


    @staticmethod
    def _get_comp(line):
        s = line.split("=")[int('=' in line)]
        s = s.split(";")[int(~(';' in line))]
        return C.comp_map[s]


    @staticmethod
    def _get_jmp(line):
        if ';' in line:
            s = line.split(";")[1]
            return C.jmp_map[s] 
        else:
            return '000'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str) 
    args = parser.parse_args()

    asm = HackAssembler(args.input)
    asm.setup()
    asm.replace_symbols()
    asm.code()
    asm.write()
    print('done!')


if __name__ == "__main__":
    main()
