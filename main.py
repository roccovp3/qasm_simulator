# QASM SIMULATOR
import sys
import numpy as np

def main():
    input_str = get_input()
    instr_array = create_instr_array(input_str)
    print(instr_array)
    parse_instr_args(instr_array)
    return 0


def get_input():
    input_str = ""
    print(sys.argv[1:])
    for arg in sys.argv[1:]:
        try:
            file = open(arg, 'r')
            for line in file.readlines():
                if "(" in line and ")" in line:
                    line = line[0:line.index('(')]+line[line.index('('):line.index(')')].replace(' ', '')+line[line.index(')'):]
                if "//" in line and ";" in line:
                    if line[::-1].index("//") < line[::-1].index(";"): #if comment is before
                        line = line[0:line.index(";")+1]+'\n'
                elif "//" in line and ";" not in line:
                    continue
                input_str += line
        except FileNotFoundError:
            print("Invaild Input")
    print("Input String:", input_str)
    input_str = input_str.replace('\n', '')
    return input_str


def create_instr_array(input_str):
    instr_array = input_str.split(";")
    instr_array = [x.strip().split(' ') for x in instr_array if (x != '')]
    return instr_array


def parse_instr_args(instr_array):
    supported_instrs = ['u', 'id', 'x', 'h', 's', 'sdg', 'z', 't', 'tdg', 'q', 'qdg', 'measure']
    for instr in instr_array:
        if instr[0][0] == 'u':
            parse_u_gate(instr[0])
        #ADD ALL GATES
        else:
            print("Invalid/Unsupported Instruction")

def parse_u_gate(gate):
    gate_args = gate[2:gate.index(')')].split(',')
    for i, arg in enumerate(gate_args):
        gate_args[i] = eval(arg.replace("pi", str(np.pi)))
    print(gate_args)
    return

if __name__ == '__main__':
    main()

