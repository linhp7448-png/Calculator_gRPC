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


        buttons = [
            ['7', '8', '9', '/', 'sqrt'],
            ['4', '5', '6', '*', '('],
            ['1', '2', '3', '-', ')'],
            ['0', '.', '=', '+', 'x'],
            ['sin', 'cos', 'tan', 'log', 'C']
        ]

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

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
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
    gui = CalculatorGUI()
    gui.run()
