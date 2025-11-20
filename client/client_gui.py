import sys, os, grpc, tkinter as tk
<<<<<<< HEAD
from tkinter import ttk, messagebox, scrolledtext
=======
from tkinter import ttk, messagebox
try:
    import ttkthemes as tkm
    THEMED_TK = True
except ImportError:
    THEMED_TK = False
    print("Warning: ttkthemes not installed. Falling back to default tkinter theme.")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
>>>>>>> 5d636829592fffd62425267562282d2cc7e654fe

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from proto import calculator_pb2, calculator_pb2_grpc


class CalculatorClient:
    def __init__(self):
        channel = grpc.insecure_channel('localhost:50051')
        self.stub = calculator_pb2_grpc.CalculatorServiceStub(channel)

    def calculate(self, expression):
        request = calculator_pb2.CalculatorRequest(expression=expression)
        response = self.stub.Calculate(request)
        if response.error:
            return f"Error: {response.error}"
        return response.result

class CalculatorGUI:
    def __init__(self):
        self.client = CalculatorClient()
<<<<<<< HEAD
        self.window = tk.Tk()
        self.window.title("Scientific Calculator (gRPC)")
        self.window.geometry("600x950")
        self.window.configure(bg="#f4f4f4")

        self.expression = ""
        self.history = []
        self.history_index = -1

        # ======================
        # ENTRY
        # ======================
        self.entry = tk.Entry(
            self.window, font=("Consolas", 40),
            justify='right', bd=5, relief="sunken"
        )
        self.entry.pack(fill='x', padx=20, pady=20, ipady=20)

        # ======================
        # DROPDOWN CHUYỂN ĐỔI
        # ======================
        convert_frame = tk.Frame(self.window, bg="#f4f4f4")
        convert_frame.pack(pady=10)

        tk.Label(convert_frame, text="Chuyển đổi °C ↔ °F ↔ K",
                 font=("Arial", 22, "bold"), bg="#f4f4f4").pack()

        self.combo = ttk.Combobox(
            convert_frame,
            values=["C → F", "F → C", "C → K", "K → C", "F → K", "K → F"],
            width=20,
            font=("Arial", 18),
            state="readonly"
        )
        self.combo.set("Chọn phép chuyển đổi")
        self.combo.pack(pady=10)

        ttk.Button(
            convert_frame,
            text="Thực hiện",
            command=self.perform_convert
        ).pack()

        # ======================
        # LỊCH SỬ
        # ======================
        tk.Label(self.window, text="Lịch sử:", font=("Arial", 28, "bold"),
                 bg="#f4f4f4").pack(anchor="w", padx=20)

        self.history_box = scrolledtext.ScrolledText(
            self.window, height=5,
            font=("Consolas", 22),
            state='disabled'
        )
        self.history_box.pack(fill="both", padx=20, pady=10)

        self.history_box.bind("<Button-1>", self.on_history_click)
        self.history_box.bind("<Double-1>", self.on_history_double_click)

        # ======================
        # BÀN PHÍM
        # ======================
        button_frame = tk.Frame(self.window, bg="#f4f4f4")
        button_frame.pack(fill='both', expand=True)
=======
        
        if THEMED_TK:
            self.window = tkm.ThemedTk()
            self.window.set_theme("scidgrey") 
        else:
            self.window = tk.Tk()
            self.window.configure(bg='#f2f2f2') 
            
        self.window.title("🔢 Scientific Calculator (gRPC)")
        self.window.geometry("600x650") 
        self.window.resizable(True, True)
        
        self.expression = ""
        self.just_calculated = False
        
        display_frame = tk.Frame(self.window, bg='#ffffff')
        display_frame.pack(fill='x', padx=10, pady=20)

        display_frame.columnconfigure(0, weight=1)

        self.entry = tk.Entry(
            display_frame, 
            font=("Arial", 32, 'bold'), 
            justify='right', 
            bd=0, 
            relief=tk.FLAT, 
            bg='#ffffff', 
            fg='#333333', 
            insertbackground='#333333'
        )
        self.entry.grid(row=0, column=0, sticky='ew', ipady=30, padx=(10, 5))

        self.history_toggle_button = tk.Button(
            display_frame,
            text="🕒",
            font=("Arial", 18),
            bd=0,
            relief=tk.FLAT,
            bg='#ffffff',
            fg='#007aff',
            activebackground='#ffffff',
            activeforeground='#005bb5',
            command=self.toggle_history
        )
        self.history_toggle_button.grid(row=0, column=1, padx=(0, 10), pady=5)


        style = ttk.Style()
        style.configure('TButton', font=('Arial', 16, 'bold'), borderwidth=0, relief=tk.FLAT, padding=10)
        style.map('TButton', background=[('active', '#e0e0e0')]) 

        style.configure('Num.TButton', background='#ffffff', foreground='#333333')
        style.configure('Op.TButton', background='#e0e0e0', foreground='#007aff') 
        style.configure('Eq.TButton', background='#ffffff', foreground='#000000')
        style.configure('Func.TButton', background='#d0d0d0', foreground='#ff3b30')

>>>>>>> 5d636829592fffd62425267562282d2cc7e654fe

        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', 'x'],
            ['sin', 'cos', 'tan', 'log', 'C']
        ]

<<<<<<< HEAD
        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                btn = tk.Button(
                    button_frame, text=char,
                    font=("Arial", 22, "bold"),
                    width=4, height=2,
                    bg="white", fg="black",
                    activebackground="#ddd",
                    relief="raised", bd=3,
                    command=lambda x=char: self.on_click(x)
                )
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        for i in range(len(buttons)):
            button_frame.rowconfigure(i, weight=1)
        for i in range(len(buttons[0])):
            button_frame.columnconfigure(i, weight=1)

        # ===== PHÍM TẮT =====
        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<Return>", lambda e: self.on_click('='))
        self.window.bind("<BackSpace>", lambda e: self.on_click('⌫'))
        self.window.bind("<Escape>", lambda e: self.on_click('C'))
        self.window.bind("<Up>", self.use_previous_expression)
=======
        content_frame = tk.Frame(self.window, bg='#f2f2f2' if not THEMED_TK else None)
        content_frame.pack(expand=True, fill='both', padx=10, pady=(0, 10))
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=0)
        content_frame.rowconfigure(0, weight=1)

        frame = ttk.Frame(content_frame)
        frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        self.history_frame = tk.Frame(content_frame, bg='#f2f2f2' if not THEMED_TK else None, width=140)
        self.history_frame.grid_propagate(False)
        self.history_frame.grid(row=0, column=1, sticky='nsew')

        history_label = tk.Label(
            self.history_frame,
            text="History",
            font=("Arial", 12, 'bold'),
            bg='#f2f2f2' if not THEMED_TK else self.history_frame.cget("bg"),
            fg='#333333'
        )
        history_label.pack(anchor='n', pady=(0, 2))

        history_container = tk.Frame(self.history_frame)
        history_container.pack(expand=True, fill='both')

        self.history_listbox = tk.Listbox(
            history_container,
            font=("Arial", 12),
            bg='#ffffff',
            fg='#333333',
            activestyle='none',
            width=16
        )
        self.history_listbox.pack(side=tk.LEFT, expand=True, fill='both')
        self.history_listbox.bind('<Double-Button-1>', self._on_history_double_click)

        history_scrollbar = ttk.Scrollbar(
            history_container,
            orient=tk.VERTICAL,
            command=self.history_listbox.yview
        )
        history_scrollbar.pack(side=tk.RIGHT, fill='y')
        self.history_listbox.config(yscrollcommand=history_scrollbar.set)

        self.history_panel_visible = False
        self.history_frame.grid_remove()
        self.window.bind('<Configure>', self._on_window_change)
        self.window.bind('<Map>', lambda event: self._update_layout())
        self.window.after_idle(self._update_layout)

        for r, row in enumerate(buttons):
            for c, b in enumerate(row):
                style_name = 'Num.TButton'
                if b in ['/', '*', '-', '+', '^']:
                    style_name = 'Op.TButton'
                elif b in ['sqrt', 'sin', 'cos', 'tan', 'log']:
                    style_name = 'Op.TButton'
                elif b == 'C':
                    style_name = 'Func.TButton'
                elif b == '=':
                    style_name = 'Eq.TButton'

                ttk.Button(
                    frame, 
                    text=b, 
                    command=lambda x=b: self.on_click(x),
                    style=style_name 
                ).grid(row=r, column=c, sticky='nsew', padx=4, pady=4) 

        for i in range(5):
            frame.rowconfigure(i, weight=1)
            frame.columnconfigure(i, weight=1)
>>>>>>> 5d636829592fffd62425267562282d2cc7e654fe

    # ======================
    # XỬ LÝ CHUYỂN ĐỔI
    # ======================
    def perform_convert(self):
        mode = self.combo.get()
        if "→" not in mode:
            messagebox.showwarning("Thông báo", "Vui lòng chọn chế độ chuyển đổi!")
            return

        try:
            value = float(self.entry.get())
        except:
            messagebox.showerror("Lỗi", "Giá trị nhập không hợp lệ!")
            return

        C, F, K = None, None, None

        if mode == "C → F":
            result = value * 9/5 + 32
        elif mode == "F → C":
            result = (value - 32) * 5/9
        elif mode == "C → K":
            result = value + 273.15
        elif mode == "K → C":
            result = value - 273.15
        elif mode == "F → K":
            result = (value - 32) * 5/9 + 273.15
        elif mode == "K → F":
            result = (value - 273.15) * 9/5 + 32

        self.expression = str(result)
        self.update_entry()

    # ======================
    # LỊCH SỬ
    # ======================
    def on_history_click(self, event):
        index = self.history_box.index("@%s,%s" % (event.x, event.y))
        line = self.history_box.get(index + " linestart", index + " lineend")
        if "=" in line:
            expr = line.split("=")[0].strip()
            self.expression = expr
            self.update_entry()

    def on_history_double_click(self, event):
        index = self.history_box.index("@%s,%s" % (event.x, event.y))
        line = self.history_box.get(index + " linestart", index + " lineend")
        if "=" in line:
            result = line.split("=")[1].strip()
            self.expression = result
            self.update_entry()

    # ======================
    # MŨI TÊN LÊN
    # ======================
    def use_previous_expression(self, event):
        if not self.history:
            return

        if self.history_index == -1:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)

        expr = self.history[self.history_index].split("=")[0].strip()
        self.expression = expr
        self.update_entry()

    # ======================
    # XỬ LÝ NÚT
    # ======================
    def on_click(self, char):
        if char == 'C':
            self.expression = ""
<<<<<<< HEAD
            self.update_entry()
            return

        if char == '⌫':
            self.expression = self.expression[:-1]
            self.update_entry()
            return

        if char == '=':
            try:
                result = self.client.calculate(self.expression)
                self.add_to_history(self.expression, result)
                self.expression = str(result)
                self.history_index = -1
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.expression = ""
            self.update_entry()
            return

        self.expression += char
        self.update_entry()

    # ======================
    def on_key_press(self, event):
        if event.char in "0123456789+-*/().^":
            self.expression += event.char
            self.update_entry()

    def add_to_history(self, expr, result):
        line = f"{expr} = {result}"
        self.history.append(line)

        self.history_box.config(state='normal')
        self.history_box.insert(tk.END, line + "\n")
        self.history_box.config(state='disabled')
        self.history_box.yview_moveto(1)

    def update_entry(self):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.expression)

=======
            self.just_calculated = False 

        elif char == 'x':
            self.expression = self.expression[:-1] 
            self.just_calculated = False 

        elif char == '=':
            try:
                current_expression = self.expression
                response = self.client.stub.Calculate(
                    calculator_pb2.CalculatorRequest(expression=current_expression)
                )
                self.expression = str(response.result)
                self._add_to_history(current_expression, self.expression)
                self.just_calculated = True 
            
            except grpc.RpcError as e:
                messagebox.showerror(f"Lỗi Server ({e.code()})", e.details())
                self.expression = ""
                self.just_calculated = False 
            except Exception as e:
                messagebox.showerror("Lỗi Client", str(e))
                self.expression = ""
                self.just_calculated = False 
        
        else: 
            
            if self.just_calculated:
                if char in ['/', '*', '-', '+']:
                    self.expression += char
                else:
                    self.expression = char
                
                self.just_calculated = False
            
            else:
                self.expression += char
        
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

>>>>>>> 5d636829592fffd62425267562282d2cc7e654fe
    def run(self):
        self.window.mainloop()

    def _add_to_history(self, expression, result):
        if expression.strip():
            self.history_listbox.insert(tk.END, f"{expression} = {result}")
            self.history_listbox.yview_moveto(1.0)

    def toggle_history(self):
        if self.window.state() == 'zoomed':
            return
        if self.history_panel_visible:
            self._hide_history_panel()
        else:
            self._show_history_panel()
        self._update_layout()

    def _show_history_panel(self):
        if not self.history_frame.winfo_ismapped():
            self.history_frame.grid(row=0, column=1, sticky='nsew')
        self.history_panel_visible = True
        if self.window.state() != 'zoomed':
            self.history_toggle_button.config(relief=tk.SUNKEN)

    def _hide_history_panel(self):
        if self.history_frame.winfo_ismapped():
            self.history_frame.grid_remove()
        self.history_panel_visible = False
        if self.window.state() != 'zoomed':
            self.history_toggle_button.config(relief=tk.FLAT)

    def _update_layout(self):
        maximized = self.window.state() == 'zoomed'
        if maximized:
            if self.history_panel_visible is False:
                self._show_history_panel()
            if self.history_toggle_button.winfo_ismapped():
                self.history_toggle_button.grid_remove()
            self.history_toggle_button.config(relief=tk.FLAT)
        else:
            if not self.history_toggle_button.winfo_ismapped():
                self.history_toggle_button.grid()
            if self.history_panel_visible:
                if not self.history_frame.winfo_ismapped():
                    self.history_frame.grid(row=0, column=1, sticky='nsew')
                self.history_toggle_button.config(relief=tk.SUNKEN)
            else:
                if self.history_frame.winfo_ismapped():
                    self.history_frame.grid_remove()
                self.history_toggle_button.config(relief=tk.FLAT)

    def _on_window_change(self, event):
        if event.widget is self.window:
            self._update_layout()

    def _on_history_double_click(self, event):
        selection = self.history_listbox.curselection()
        if not selection:
            return
        item = self.history_listbox.get(selection[0])
        if '=' in item:
            result = item.split('=', 1)[1].strip()
        else:
            result = item.strip()
        self.expression = result
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

if __name__ == "__main__":
    CalculatorGUI().run()
