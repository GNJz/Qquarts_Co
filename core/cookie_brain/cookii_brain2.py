
# ---------------------
# 📦 IMPORTS
# ---------------------
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt

# ---------------------
# 🧠 팝업 함수
# ---------------------
def show_brain_popup(state_list):
    root = tk.Tk()
    root.withdraw()
    message = "\n".join(state_list)
    messagebox.showinfo("🧠 Cookii 뇌 상태", message)
    root.destroy()

# ---------------------
# 🧠 뉴런 클래스
# ---------------------
class CookiiNeuron:
    def __init__(self, label):
        self.label = label
        self.state = 0
        self.history = []

    def stimulate(self, signal):
        if signal == "pain":
            self.state = -1
        elif signal == "calm":
            self.state = 0
        elif signal == "interest":
            self.state = 1
        elif signal == "focus":
            self.state = 2
        self.history.append(self.state)

# ---------------------
# 🧠 브레인 클래스
# ---------------------
class CookiiBrain:
    def __init__(self):
        self.neurons = [
            CookiiNeuron("N0"),
            CookiiNeuron("N1"),
            CookiiNeuron("N2"),
            CookiiNeuron("N3"),
            CookiiNeuron("N4")
        ]

    def perceive(self, stimulus):
        for neuron in self.neurons:
            neuron.stimulate(stimulus)

    @property
    def history(self):
        return [neuron.history for neuron in self.neurons]

    def think(self):
        return [f"{n.label}:{n.state}" for n in self.neurons]

# ---------------------
# 📊 분석 함수
# ---------------------
def analyze(brain, filename="cookii_brain.png"):
    plt.figure(figsize=(8, 4))
    states = brain.history
    labels = [n.label for n in brain.neurons]

    for i, state in enumerate(states):
        plt.plot(state, label=labels[i], marker='o')

    plt.title("🧠 Cookii Neuron Activity Over Time")
    plt.xlabel("Time Step")
    plt.ylabel("State (-1: pain, 0: calm, 1: interest, 2: focus)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"🧠 뇌 활동 이미지 저장됨: {filename}")

# ---------------------
# 🚀 실행부
# ---------------------
if __name__ == "__main__":
    brain = CookiiBrain()

    while True:
        stimulus = input("💡 자극 입력 (interest, focus, pain, calm / 종료: q): ")
        if stimulus == "q":
            print("🔚 종료합니다.")
            break
        if stimulus not in ["interest", "focus", "pain", "calm"]:
            print("⚠️ 유효한 자극이 아닙니다. 다시 입력하세요.")
            continue

        brain.perceive(stimulus)
        current_state = brain.think()
        print("🧠 현재 상태:", current_state)
        show_brain_popup(current_state)

    analyze(brain)