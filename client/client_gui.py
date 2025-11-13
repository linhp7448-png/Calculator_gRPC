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
        self.window.title("🔢 Scientific Calculator (gRPC)")
        self.window.geometry("480x680")
        self.window.resizable(True, True)

        # Biểu thức và lịch sử
        self.expression = ""
        self.history = []

        # Entry hiển thị biểu thức
        self.entry = ttk.Entry(self.window, font=("Consolas", 24), justify='right')
        self.entry.pack(fill='x', padx=10, pady=10, ipady=15)

        # Khu vực hiển thị lịch sử
        ttk.Label(self.window, text="Lịch sử tính toán:", font=("Arial", 11, "bold")).pack(anchor="w", padx=10)
        self.history_box = scrolledtext.ScrolledText(self.window, height=6, font=("Consolas", 12), state='disabled')
        self.history_box.pack(fill='both', expand=False, padx=10, pady=5)

        # Các nút
        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', '('],
            ['0', '.', '=', '+', ')'],
            ['sin', 'cos', 'tan', 'log', 'C', '⌫']
        ]

        frame = ttk.Frame(self.window)
        frame.pack(expand=True, fill='both')

        for r, row in enumerate(buttons):
            for c, b in enumerate(row):
                ttk.Button(
                    frame, text=b, command=lambda x=b: self.on_click(x)
                ).grid(row=r, column=c, sticky='nsew', padx=3, pady=3, ipadx=5, ipady=10)

        for i in range(len(buttons)):
            frame.rowconfigure(i, weight=1)
        for j in range(len(buttons[0])):
            frame.columnconfigure(j, weight=1)

        # Ràng buộc bàn phím
        self.window.bind("<Key>", self.on_key_press)
        self.window.bind("<Return>", lambda e: self.on_click('='))
        self.window.bind("<BackSpace>", lambda e: self.on_click('⌫'))
        self.window.bind("<Escape>", lambda e: self.on_click('C'))

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '⌫':
            self.expression = self.expression[:-1]
        elif char == '=':
            try:
                result = self.client.calculate(self.expression)
                self.add_to_history(self.expression, result)
                self.expression = str(result)
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.expression = ""
        else:
            self.expression += char

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def on_key_press(self, event):
        key = event.char
        allowed_chars = "0123456789+-*/().^"
        if key in allowed_chars:
            self.expression += key
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)

    def add_to_history(self, expression, result):
        self.history.append(f"{expression} = {result}")
        self.history_box.config(state='normal')
        self.history_box.insert(tk.END, f"{expression} = {result}\n")
        self.history_box.config(state='disabled')
        self.history_box.yview_moveto(1)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = CalculatorGUI()
    gui.run()
