from clvm_rs import Program

from . import load_resource


def main():
    program = Program.fromhex(load_resource("sha256tree.hex", __package__).decode())
    print(program)


if __name__ == '__main__':
    main()