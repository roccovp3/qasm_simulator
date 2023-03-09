# QASM SIMULATOR
import sys
import numpy as np
from qubit import Qubit

QREGS = {}
CREGS = {}

CREGS_ALL_SHOTS = {}
def main():
    shots = 1024 #hard coded for now, will be a user input later
    for shot in range(shots):
        QREGS.clear()
        CREGS.clear()
        input_str = get_input()
        instr_array = create_instr_array(input_str)
        print(instr_array)
        for instr in instr_array:
            execute_instr(instr)
            for key, value in QREGS.items():
                print(key, ":", value)
            for key, value in CREGS.items():
                print(key, ":", value)
        for key, value in CREGS.items():
            try:
                CREGS_ALL_SHOTS[key][value] += 1
            except KeyError:
                CREGS_ALL_SHOTS.update({key: [0, 0]})
                CREGS_ALL_SHOTS[key][value] += 1
        print(CREGS_ALL_SHOTS)
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
                    if line.index("//") > line.index(";"): #if comment is after
                        line = line[0:line.index(";")+1]+'\n'
                    else:
                        line = ""
                elif "//" in line and ";" not in line:
                    line = ""
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


def execute_instr(instr):
    supported_instrs = ['qreg', 'creg', 'u', 'id', 'x', 'h', 's', 'sdg', 'z', 't', 'tdg', 'q', 'qdg', 'measure']
    p = 0.2
    if instr[0][0] == 'u':
        theta, phi, lamb = parse_u_gate(instr[0])
        QREGS[instr[1]].applyUnitaryGate(theta, phi, lamb)
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'x':
        QREGS[instr[1]].applyXGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'h':
        QREGS[instr[1]].applyHGate()
        #QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 's':
        QREGS[instr[1]].applySGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'sdg':
        QREGS[instr[1]].applySdgGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 't':
        QREGS[instr[1]].applyTGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'tdg':
        QREGS[instr[1]].applyTdgGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'q':
        QREGS[instr[1]].applyQGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'qdg':
        QREGS[instr[1]].applyQdgGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'z':
        QREGS[instr[1]].applyZGate()
        QREGS[instr[1]].applyNoisyGate(p)
    elif instr[0] == 'creg':
        CREGS.update({instr[1]: 0})
    elif instr[0] == 'qreg':
        QREGS.update({instr[1]: Qubit(1, 0)})
    elif instr[0] == 'measure':
        CREGS[instr[3]] = QREGS[instr[1]].measureHV(1/np.sqrt(2))
    else:
        print("Invalid/Unsupported Instruction")


def parse_u_gate(gate):
    # parse
    gate_args = gate[2:gate.index(')')].split(',')
    for i, arg in enumerate(gate_args):
        gate_args[i] = eval(arg.replace("pi", str(np.pi)))

    # create array
    theta = gate_args[0]
    phi = gate_args[1]
    lamb = gate_args[2]
    return theta, phi, lamb


if __name__ == '__main__':
    main()

