
import tkinter as tk
import random

class TasteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart 혀 Taste Analyzer")
        self.tastes = ['Sweet', 'Salty', 'Sour', 'Bitter', 'Umami']
        self.bars = {}

        for idx, taste in enumerate(self.tastes):
            label = tk.Label(root, text=taste, font=("Helvetica", 14))
            label.grid(row=idx, column=0, padx=10, pady=5)

            bar = tk.Scale(root, from_=0, to=10, orient='horizontal', length=200, 
                           troughcolor='lightgray', fg='blue')
            bar.grid(row=idx, column=1)
            self.bars[taste] = bar

        self.button = tk.Button(root, text="🔍 맛 분석", command=self.analyze)
        self.button.grid(row=len(self.tastes), column=0, columnspan=2, pady=20)

        self.result = tk.Label(root, text="", font=("Helvetica", 12))
        self.result.grid(row=len(self.tastes)+1, column=0, columnspan=2)

    def analyze(self):
        result_text = "📊 Taste Output:\n"
        for taste in self.tastes:
            val = self.bars[taste].get()
            bar = '█' * val + '-' * (10 - val)
            result_text += f"{taste:<6}: {bar} ({val})\n"
        self.result.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TasteApp(root)
    root.mainloop()