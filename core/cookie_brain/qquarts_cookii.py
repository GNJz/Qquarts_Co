from matplotlib import pyplot as plt

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

    def __repr__(self):
        return f"{self.label}:{self.state}"

class CookiiBrain:
    def __init__(self):
        self.neurons = [CookiiNeuron(f"N{i}") for i in range(5)]

    def perceive(self, stimulus):
        for neuron in self.neurons:
            neuron.stimulate(stimulus)

    def think(self):
        return [str(n) for n in self.neurons]

def analyze(brain, filename="cookii_brain.png"):
    plt.figure(figsize=(8, 4))
    states = [n.history for n in brain.neurons]
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
    print(f"📊 뇌 활동 이미지 저장됨: {filename}")

# 🚀 실행 부분
if __name__ == "__main__":
    brain = CookiiBrain()
    stimuli = ["interest", "focus", "pain", "calm"]
    for stimulus in stimuli:
        print(f"\n🔶 자극: {stimulus}")
        brain.perceive(stimulus)
        print("🧠 현재 상태:", brain.think())

    analyze(brain)from matplotlib import pyplot as plt

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

    def __repr__(self):
        return f"{self.label}:{self.state}"

class CookiiBrain:
    def __init__(self):
        self.neurons = [CookiiNeuron(f"N{i}") for i in range(5)]

    def perceive(self, stimulus):
        for neuron in self.neurons:
            neuron.stimulate(stimulus)

    def think(self):
        return [str(n) for n in self.neurons]

def analyze(brain, filename="cookii_brain.png"):
    plt.figure(figsize=(8, 4))
    states = [n.history for n in brain.neurons]
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
    print(f"📊 뇌 활동 이미지 저장됨: {filename}")

# 🚀 실행 부분
if __name__ == "__main__":
    brain = CookiiBrain()
    stimuli = ["interest", "focus", "pain", "calm"]
    for stimulus in stimuli:
        print(f"\n🔶 자극: {stimulus}")
        brain.perceive(stimulus)
        print("🧠 현재 상태:", brain.think())

    analyze(brain)