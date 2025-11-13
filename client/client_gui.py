import sys, os, grpc, tkinter as tk
from tkinter import ttk, messagebox
try:
    import ttkthemes as tkm
    THEMED_TK = True
except ImportError:
    THEMED_TK = False
    print("Warning: ttkthemes not installed. Falling back to default tkinter theme.")

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
        
        if THEMED_TK:
            self.window = tkm.ThemedTk()
            self.window.set_theme("scidgrey") 
        else:
            self.window = tk.Tk()
            self.window.configure(bg='#f2f2f2') 
            
        self.window.title("🔢 Scientific Calculator (gRPC)")
        self.window.geometry("400x650") 
        self.window.resizable(True, True)
        
        self.expression = ""
        
        self.entry = tk.Entry(
            self.window, 
            font=("Arial", 32, 'bold'), 
            justify='right', 
            bd=0, 
            relief=tk.FLAT, 
            bg='#ffffff', 
            fg='#333333', 
            insertbackground='#333333'
        )
        display_frame = tk.Frame(self.window, bg='#ffffff')
        display_frame.pack(fill='x', padx=10, pady=20)
        self.entry.pack(fill='x', ipady=30, padx=10) 


        style = ttk.Style()
        style.configure('TButton', font=('Arial', 16, 'bold'), borderwidth=0, relief=tk.FLAT, padding=10)
        style.map('TButton', background=[('active', '#e0e0e0')]) 

        style.configure('Num.TButton', background='#ffffff', foreground='#333333')
        style.configure('Op.TButton', background='#e0e0e0', foreground='#007aff') 
        style.configure('Eq.TButton', background='#007aff', foreground='white')
        style.configure('Func.TButton', background='#d0d0d0', foreground='#ff3b30')


        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '^'],
            ['1', '2', '3', '-', '('],
            ['0', '.', '=', '+', ')'],
            ['sin', 'cos', 'tan', 'log', 'C']
        ]

        frame = ttk.Frame(self.window)
        frame.pack(expand=True, fill='both', padx=10, pady=5)

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

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                result = self.client.calculate(self.expression)
                self.expression = str(result)
            except Exception as e:
                messagebox.showerror("Lỗi gRPC/Server", str(e))
                self.expression = ""
        else:
            self.expression += char
        
        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = CalculatorGUI()
    gui.run()
