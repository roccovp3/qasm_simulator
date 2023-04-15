# QASM SIMULATOR
import sys
import numpy as np
from qubit import Qubit
import math
import random
import re

QREGS = {}
CREGS = {}

CREGS_ALL_SHOTS = {}
statevector = np.array([1])

def compute(shots, code):
    global statevector
    statevector = [1]
    CREGS_ALL_SHOTS.clear()
    input_str = get_input(code)
    for shot in range(shots):
        QREGS.clear()
        CREGS.clear()
        statevector = [1]
        instr_array = create_instr_array(input_str)
        #print(instr_array)
        for instr in instr_array:
            execute_instr(instr)
            for key, value in QREGS.items():
                continue
                #print(key, ":", value)
            for key, value in CREGS.items():
                continue
                #print(key, ":", value)
        for key, value in CREGS.items():
            try:
                CREGS_ALL_SHOTS[key][value] += 1
            except KeyError:
                CREGS_ALL_SHOTS.update({key: [0, 0]})
                CREGS_ALL_SHOTS[key][value] += 1
        #print(CREGS_ALL_SHOTS)
    return CREGS_ALL_SHOTS;


def get_input(code):
    input_str = ""
    try:
        input_str = code
        input_str_no_comments = ''
        for line in input_str.split('\n'):
            if "(" in line and ")" in line:
                line = line[0:line.index('(')] + line[line.index('('):line.index(')')].replace(' ', '') + line[
                                                                                                          line.index(
                                                                                                              ')'):]
            if "//" in line and ";" in line:
                if line.index("//") > line.index(";"):  # if comment is after
                    line = line[0:(len(line) - 1 - line[::-1].index(';')) + 1] + '\n'
                else:
                    line = ""
            elif "//" in line and ";" not in line:
                line = ""
            input_str_no_comments += line
        input_str_no_comments = input_str_no_comments.replace('\n', '')
        input_str_no_comments = input_str_no_comments.replace('\r', '')
        #print(input_str_no_comments)
    except FileNotFoundError:
        print("Invaild Input")
    print("Input String:", input_str)

    return input_str_no_comments


def create_instr_array(input_str):
    instr_array = input_str.split(";")
    instr_array = [re.split(',|\s', x.strip()) for x in instr_array]
    for i, x in enumerate(instr_array):
        instr_array[i] = [y for y in x if y != '']
    for x in instr_array:
        if x == []:
            instr_array.remove(x)
    #print(instr_array)
    return instr_array

def execute_instr(instr):
    supported_instrs = ['qreg', 'creg', 'u', 'id', 'x', 'h', 's', 'sdg', 'z', 't', 'tdg', 'q', 'qdg', 'measure', 'cx']
    global statevector
    if instr[0][0] == 'u':
        theta, phi, lamb = parse_u_gate(instr[0])
        U = createGateMatrix(theta, phi, lamb, instr)
        statevector = np.matmul(U, statevector)
    elif instr[0] == 'x':
        U = createGateMatrix(np.pi, 0, np.pi, instr)
        statevector = np.matmul(U, statevector)
    elif instr[0] == 'h':
        U = createGateMatrix(np.pi/2, 0, np.pi, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 's':
        U = createGateMatrix(0, 0, np.pi/2, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'sdg':
        U = createGateMatrix(0, 0, -np.pi/2, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 't':
        U = createGateMatrix(0, 0, np.pi/4, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'tdg':
        U = createGateMatrix(0, 0, -np.pi/4, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'q':
        U = createGateMatrix(np.pi/2, np.pi/2, np.pi, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'qdg':
        U = createGateMatrix(np.pi/2, 0, np.pi/2, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'z':
        U = createGateMatrix(0, np.pi, 0, instr)
        statevector = U.dot(statevector)
    elif instr[0] == 'creg':
        CREGS.update({instr[1]: 0})
    elif instr[0] == 'qreg':
        QREGS.update({instr[1]: Qubit(1, 0)})
        statevector = np.kron([1,0], statevector)
    elif instr[0] == 'measure':
        threshold = -0.5*np.log(1 - np.sqrt(1-1/np.sqrt(2)))
        enumQREGS = {}
        for i, (k,v) in enumerate(QREGS.items()):
            enumQREGS[k] = i
        p0 = 0
        p1 = 0
        #print(statevector)
        for i in range(0, len(statevector)):
            if ((i//(2**enumQREGS[instr[1]])) % 2) == 0:
                p0 += abs(statevector[i])**2
        p1 = 1 - p0
        #print(p0)
        if p0 <= threshold and p1 <= threshold:
            CREGS[instr[3]] = random.randint(0,1) # no detection (invalid measurement)
        elif p0 > threshold and p1 <= threshold:
            CREGS[instr[3]] = 0 # single H qubit detected
        elif p0 <= threshold and p1 > threshold:
            CREGS[instr[3]] = 1 # single V qubit detected
        else:
            CREGS[instr[3]] = random.randint(0,1) # multiple detections (invalid measurement)

    #https://quantumcomputing.stackexchange.com/questions/5179/how-to-construct-matrix-of-regular-and-flipped-2-qubit-cnot
    elif instr[0] == 'cx': #CNOT
        cnot0 = [1]
        cnot1 = [1]
        for qubit in QREGS.keys():
            #print(qubit)
            if qubit == instr[1]:
                cnot0 = np.kron(cnot0, np.array([[1, 0], [0, 0]]))
                cnot1 = np.kron(cnot1, np.array([[0, 0], [0, 1]]))
            elif qubit == instr[2]:
                cnot0 = np.kron(cnot0, np.eye(2))
                cnot1 = np.kron(cnot1, np.array([[0, 1], [1, 0]]))
            else:
                cnot1 = np.kron(cnot1, np.eye(2))
                cnot0 = np.kron(cnot0, np.eye(2))
        cnot = cnot0 + cnot1
        statevector = cnot.dot(statevector)

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

def createGateMatrix(theta, phi, lamb, instr):
    U = [[0, 0], [0, 0]]
    z1 = np.exp(1j * phi)
    z2 = -np.exp(1j * lamb)
    z3 = np.exp(1j * (lamb + phi))
    U[0][0] = np.cos(theta / 2)
    U[1][0] = np.sin(theta / 2) * z1
    U[0][1] = np.sin(theta / 2) * z2
    U[1][1] = np.cos(theta / 2) * z3
    u = np.array([1])
    for qubit in QREGS.keys():
        #print(qubit)
        if qubit == instr[1]:
            u = np.kron(u, U)
        else:
            u = np.kron(u, np.array([[1, 0], [0, 1]]))
    #print(u)
    return u
