import sys

from machine import Machine

def usage():
    print("Usage:")
    print(" python3 main.py <filename>.obj")
    sys.exit(1)

def main():
    if len(sys.argv) != 2:
        usage()

    obj_file = sys.argv[1]

    try:
        print("Loading program ...")
        with open(obj_file, 'r') as f:
            machine = Machine()
            if not machine.load_section(f):
                print("Error loading object file")
                return

    except FileNotFoundError:
        print(f"File not found: {obj_file}")
        return

    print(f"Program loaded.")
    print(f"Initial PC = {machine.get_pc():#06x}")
    
    print("Starting execution (Ctrl+C to stop) ...")

    try:
        while True:
            machine.execute()
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
        print(f"Final PC = {machine.get_pc():#06x}")


if __name__ == "__main__":
    main()