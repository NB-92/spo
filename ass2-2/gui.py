import tkinter as tk
from tkinter import ttk

from machine import Machine

print("GUI start")

# ustvari window
root = tk.Tk()
root.title("SIC/XE Simulator")
root.geometry("1200x800")

main_frame = ttk.Frame(root)
main_frame.pack(side="left", fill="y", padx=10, pady=10)

# REGISTRI
# funkcija, ki refresha vse vrednosti registrov, in s tem tudi izpis
def refreshAllRegisters():
    entries["A"].set(str(m.getA()))
    entries["X"].set(str(m.getX()))
    entries["L"].set(str(m.getL()))
    entries["B"].set(str(m.getB()))
    entries["S"].set(str(m.getS()))
    entries["T"].set(str(m.getT()))
    entries["F"].set(str(m.getF()))
    entries["PC"].set(str(m.getPC()))
    entries["SW"].set(str(m.getSW()))

regs = ["A", "X", "L", "B", "S", "T", "F", "-", "PC", "SW"]
entries = {} # slovar ("register" : "label za register")
for r in regs:
    if r == "F":
        entries[r] = tk.StringVar(value=str(m.getF()))
    else:
        entries[r] = tk.StringVar(value=str(0))

# dejanski izpis registrov
registers_frame = ttk.Frame(main_frame)
registers_frame.grid(row=0, column=0, sticky="nw", padx=10)
tk.Label(registers_frame, text="Registri:", font=("Helvetica", 12)).pack(anchor="w")
for r in regs:
    frame = ttk.Frame(registers_frame)
    frame.pack(anchor="w")

    tk.Label(frame, text=r, width=4).pack(side="left")

    value_label = tk.Label(frame, textvariable=entries[r], width=10, anchor="w")
    value_label.pack(side="left")

root.mainloop()


