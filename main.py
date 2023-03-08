# QASM SIMULATOR
import sys


def main():
    input_str = get_input()
    print(create_command_array(input_str))
    return 0


def get_input():
    input_str = ""
    print(sys.argv[1:])
    for arg in sys.argv[1:]:
        try:
            file = open(arg, 'r')
            for line in file.readlines():
                if "//" in line and ";" in line:
                    if line[::-1].index("//") < line[::-1].index(";"): #if comment is before
                        line = line[0:line.index(";")+1]+'\n'
                elif "//" in line and ";" not in line:
                    continue
                input_str += line
            #input_str += file.read()
        except FileNotFoundError:
            print("Invaild Input")
    print("Input String:", input_str)
    input_str = input_str.replace('\n', '')
    return input_str


def create_command_array(input_str):
    command_array = input_str.split(";")
    command_array = [x.strip() for x in command_array if (x != '')]
    return command_array


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
