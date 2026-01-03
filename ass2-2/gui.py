
import tkinter as tk
from tkinter import ttk
import threading
import time
from machine import Machine

class MachineGUI:

    def __init__(self, root, machine: Machine):
        self.root = root
        self.machine = machine
        self.running = False
        self.exec_thread = None

        root.title("SIC/XE Simulator")

        # REGISTRI
        regs_frame = ttk.LabelFrame(root, text="Registers")
        regs_frame.grid(column=0, row=0, padx=10, pady=10, sticky="n")

        self.reg_labels = []
        reg_names = ["A", "X", "L", "B", "S", "T", "F", "-", "PC", "SW"]

        for i, name in enumerate(reg_names):
            # imena registrov
            ttk.Label(regs_frame, text=name).grid(column=0, row=i, sticky="w")
            # vrednost registrov
            lbl = ttk.Label(regs_frame, width=12)
            lbl.grid(column=1, row=i)
            self.reg_labels.append(lbl)

        # POMNILNIK
        self.mem_base = 0x000000
        self.mem_size = 0x100 # 256 bajtov

        mem_frame = ttk.LabelFrame(root, text="Memory")
        mem_frame.grid(column=1, row=0, padx=10, pady=10)

        mem_btn_frame = ttk.Frame(mem_frame)
        mem_btn_frame.pack(pady=5)

        ttk.Button(mem_btn_frame, text="▲", width=5, command=self.mem_up).grid(row=0, column=0, padx=2)
        ttk.Button(mem_btn_frame, text="▼", width=5, command=self.mem_down).grid(row=0, column=1, padx=2)
        ttk.Button(mem_btn_frame, text="O", width=5, command=self.mem_start).grid(row=0, column=2, padx=2)

        self.mem_text = tk.Text(mem_frame, width=60, height=16)
        self.mem_text.pack()

        # GUMBI
        btn_frame = ttk.Frame(root)
        btn_frame.grid(column=0, row=1, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="STEP", command=self.step).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="START", command=self.start).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="STOP", command=self.stop).grid(row=0, column=2, padx=5)

        # DISASSEMBLY
        dis_frame = ttk.LabelFrame(root, text="Disassembly")
        dis_frame.grid(column=2, row=0, padx=10, pady=10, sticky="n")

        self.dis_text = tk.Text(dis_frame, width=40, height=20)
        self.dis_text.tag_configure("current_pc", background="light blue")
        self.dis_text.pack()

        self.update()

    # POSODOBITEV PRIKAZA
    def update(self):
        # registri
        for i, lbl in enumerate(self.reg_labels):
            val = self.machine.get_reg(i)
            if i == 8: #PC
                lbl.config(text=f"{val:#06x}")
            else:
                lbl.config(text=str(val))

        # pomnilnik (prvih 256 bajtov)
        self.mem_text.delete("1.0", tk.END)
        start = self.mem_base
        end = self.mem_base + self.mem_size
        for addr in range(start, end, 16):
            bytes_row = " ".join(f"{self.machine.get_byte(addr + i):02X}" for i in range(16))
            self.mem_text.insert(tk.END, f"{addr:06x}: {bytes_row}\n")

        # disassebly
        self.dis_text.delete("1.0", tk.END)

        pc = self.machine.get_pc()
        addr = pc

        for _ in range(15): # pokazi 15 ukazov
            size, text = self.machine.disassemble(addr)
            if addr == pc:
                self.dis_text.insert(tk.END, f" {text}\n", "current_pc")
            else:
                self.dis_text.insert(tk.END, f" {text}\n")
            addr += size

    # POMNILNIK
    def mem_up(self):
        self.mem_base = max(0, self.mem_base - self.mem_size)
        self.update()

    def mem_down(self):
        max_addr = len(self.machine.memory) - self.mem_size
        self.mem_base = min(max_addr, self.mem_base + self.mem_size)
        self.update()

    def mem_start(self):
        self.mem_base = 0
        self.update()

    # UKAZI
    def step(self):
        self.machine.step()
        self.update()

    def start(self):
        if self.running:
            return
        self.running = True
        self.exec_thread = threading.Thread(target=self.run_loop, daemon=True)
        self.exec_thread.start()

    def stop(self):
        self.running = False
        self.machine.stop()

    def run_loop(self):
        while self.running:
            ok = self.machine.execute()
            if not ok:
                self.running = False
                break
            self.root.after(0, self.update)
            time.sleep(0.1) # hitrost izvajanja