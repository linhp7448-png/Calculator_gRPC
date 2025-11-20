import sys, os, grpc, tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

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
        self.window = tk.Tk()
        self.window.title("Scientific Calculator (gRPC)")
        self.window.geometry("600x950")
        self.window.configure(bg="#f4f4f4")

        self.expression = ""
        self.history = []
        self.history_index = -1

        # ENTRY
        self.entry = tk.Entry(
            self.window,
            font=("Consolas", 32),
            justify='right',
            bd=5,
            relief="sunken"
        )
        self.entry.pack(fill='x', padx=20, pady=20, ipady=20)

        # DROPDOWN
        convert_frame = tk.Frame(self.window, bg="#f4f4f4")
        convert_frame.pack(pady=10)

        tk.Label(
            convert_frame,
            text="Chuyển đổi °C ↔ °F ↔ K",
            font=("Arial", 22, "bold"),
            bg="#f4f4f4"
        ).pack()

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

        # LỊCH SỬ
        tk.Label(
            self.window,
            text="Lịch sử:",
            font=("Arial", 28, "bold"),
            bg="#f4f4f4"
        ).pack(anchor="w", padx=20)

        self.history_box = scrolledtext.ScrolledText(
            self.window,
            height=3,
            font=("Consolas", 22),
            state='disabled'
        )
        self.history_box.pack(fill="both", padx=20, pady=10)
        self.history_box.bind("<Button-1>", self.on_history_click)
        self.history_box.bind("<Double-1>", self.on_history_double_click)

        # BÀN PHÍM
        button_frame = tk.Frame(self.window, bg="#f4f4f4")
        button_frame.pack(fill='both', expand=True)

        style = ttk.Style()
        style.configure('Num.TButton', font=("Arial", 22), background='#ffffff', foreground='#333333')
        style.configure('Op.TButton', font=("Arial", 22), background='#e0e0e0', foreground='#007aff')
        style.configure('Func.TButton', font=("Arial", 22), background='#d0d0d0', foreground='#ff3b30')

        buttons = [
            ['7', '8', '9', '/', '√', '%'],
            ['4', '5', '6', '*', '^', 'π'],
            ['1', '2', '3', '-', '(', ')'],
            ['0', '.', '=', '+', '| |', 'ln'],
            ['sin', 'cos', 'tan', 'log', 'C', '⌫']
        ]

        for r, row in enumerate(buttons):
            for c, char in enumerate(row):
                if char in ['+', '-', '*', '/', '^', '√','(', ')','π', '%']:
                    style_name = 'Op.TButton'
                elif char in ['sin', 'cos', 'tan', 'log', 'C', '⌫', 'ln', '| |']:
                    style_name = 'Func.TButton'
                else:
                    style_name = 'Num.TButton'

                btn = ttk.Button(
                    button_frame,
                    text=char,
                    style=style_name,
                    command=lambda x=char: self.on_click(x)
                )
                btn.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")

        for i in range(len(buttons)):
            button_frame.rowconfigure(i, weight=1)
        for i in range(len(buttons[0])):
            button_frame.columnconfigure(i, weight=1)

        # PHÍM TẮT
        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<Return>", lambda e: self.on_click('='))
        self.window.bind("<BackSpace>", lambda e: self.on_click('⌫'))
        self.window.bind("<Escape>", lambda e: self.on_click('C'))
        self.window.bind("<Up>", self.use_previous_expression)

    # CHUYỂN ĐỔI
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

    # LỊCH SỬ
    def on_history_click(self, event):
        index = self.history_box.index("@%s,%s" % (event.x, event.y))
        line = self.history_box.get(index + " linestart", index + " lineend")
        if "=" in line:
            self.expression = line.split("=")[0].strip()
            self.update_entry()

    def on_history_double_click(self, event):
        index = self.history_box.index("@%s,%s" % (event.x, event.y))
        line = self.history_box.get(index + " linestart", index + " lineend")
        if "=" in line:
            self.expression = line.split("=")[1].strip()
            self.update_entry()

    # MŨI TÊN LÊN
    def use_previous_expression(self, event):
        if not self.history:
            return
        if self.history_index == -1:
            self.history_index = len(self.history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)

        self.expression = self.history[self.history_index].split("=")[0].strip()
        self.update_entry()

    # NÚT
    def on_click(self, char):
        if char == 'C':
            self.expression = ""
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
        if char in ['sin', 'cos', 'tan', 'log','ln']:
            self.expression += f"{char}("           
        elif char == '| |':
           self.expression += "abs("
        elif char == 'π':
           self.expression += "pi"
        elif char == '%':
           self.expression += "/100"
        elif char == '√':
           self.expression += "sqrt("
        else:
            self.expression += char
        self.update_entry()

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

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    CalculatorGUI().run()
