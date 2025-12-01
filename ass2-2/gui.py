import tkinter as tk
from tkinter import ttk
from machine import Machine

m = Machine()
print("GUI start")

# ustvari window
root = tk.Tk()
root.title("SIC/XE Simulator")
root.geometry("1200x800")

main_frame = ttk.Frame(root)
main_frame.pack(expand=True)

# REGISTRI
# funkcija, ki refresha vse vrednosti registrov
def refreshAllRegisters():
    entries["A"] = m.getA()
    entries["X"] = m.getX()
    entries["L"] = m.getL()
    entries["B"] = m.getB()
    entries["S"] = m.getS()
    entries["T"] = m.getT()
    entries["F"] = m.getF()
    entries["PC"] = m.getPC()
    entries["SW"] = m.getSW()

regs = ["A", "X", "L", "B", "S", "T", "F", "-", "PC", "SW"]
entries = {
    "A": 0,
    "X": 0,
    "L": 0,
    "B": 0,
    "S": 0,
    "T": 0,
    "F": 0.0,
    "-": 0,
    "PC": 0,
    "SW": 0
}
refreshAllRegisters()

registers_frame = ttk.Frame(main_frame)
registers_frame.grid(row=0, column=0, sticky="nw", padx=10)
tk.Label(registers_frame, text="Registri:", font=("Helvetica", 12)).pack(anchor="w")
for r in regs:
    frame = ttk.Frame(registers_frame)
    frame.pack(anchor="w")

    tk.Label(frame, text=r, width=4).pack(side="left")

    value_label = tk.Label(frame, text=entries[r], width=10, anchor="w")
    value_label.pack(side="left")


# POMNILNIK
#memory_frame = ttk.Frame(main_frame)
#memory_frame.grid(row=0, column=1, sticky="ne", padx=10)
#tk.Label(registers_frame, text="Pomnilnik:", font=("Helvetica", 12)).pack(anchor="w")

#for val in m.memory:
    #frame = ttk.Frame(memory_frame)
    #frame.pack(anchor="w")
    #tk.Label(frame, text=val, width=10, anchor="w").pack(side="left")

root.mainloop()


