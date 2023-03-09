# QASM SIMULATOR
import sys
import numpy as np
from qubit import Qubit

QREGS = {}
CREGS = {}
def main():
    input_str = get_input()
    instr_array = create_instr_array(input_str)
    for instr in instr_array:
        execute_instr(instr)
        print(QREGS['q[0]'])
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


def execute_instr(instr):
    supported_instrs = ['qreg', 'creg', 'u', 'id', 'x', 'h', 's', 'sdg', 'z', 't', 'tdg', 'q', 'qdg', 'measure']
    operations = []
    if instr[0][0] == 'u':
        theta, phi, lamb = parse_u_gate(instr[0])
        QREGS[instr[1]].applyUnitaryGate(theta, phi, lamb)
    elif instr[0] == 'x':
        QREGS[instr[1]].applyXGate()
    elif instr[0] == 'h':
        QREGS[instr[1]].applyHGate()
    elif instr[0] == 's':
        QREGS[instr[1]].applySGate()
    elif instr[0] == 'sdg':
        QREGS[instr[1]].applySdgGate()
    elif instr[0] == 't':
        QREGS[instr[1]].applyTGate()
    elif instr[0] == 'tdg':
        QREGS[instr[1]].applyTdgGate()
    elif instr[0] == 'q':
        QREGS[instr[1]].applyQGate()
    elif instr[0] == 'qdg':
        QREGS[instr[1]].applyQdgGate()
    elif instr[0] == 'z':
        QREGS[instr[1]].applyZGate()
    elif instr[0] == 'creg':
        CREGS.update({instr[1]: 0})
    elif instr[0] == 'qreg':
        QREGS.update({instr[1]: Qubit(1, 0)})
    # ADD ALL GATES
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


def apply_u_gate(gate, qubit):
    qubit.applyUnitaryGate(gate[0], gate[1], gate[2])


def applyOperation(operation):
    print(operation)


if __name__ == '__main__':
    main()

