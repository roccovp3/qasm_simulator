# QASM SIMULATOR
import sys


def main():
    input_str = get_input()

    return 0


def get_input():
    input_str = ""
    print(sys.argv[1:])
    for arg in sys.argv[1:]:
        try:
            file = open(arg, 'r')
            input_str += file.read()
        except FileNotFoundError:
            print("Invaild Input")
    print("Input String:", input_str)
    input_str.replace('\n', '')
    return input_str


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
