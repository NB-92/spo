import sys
import tkinter as tk

from machine import Machine
from gui import MachineGUI


def usage():
    print("Usage:")
    print(" python main_gui.py <filename>.obj")
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

    root = tk.Tk()
    MachineGUI(root, machine)
    root.mainloop()


if __name__ == "__main__":
    main()