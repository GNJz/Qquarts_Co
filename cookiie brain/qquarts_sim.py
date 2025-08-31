
import numpy as np
import matplotlib.pyplot as plt

class QquartsNeuron:
    def __init__(self):
        # 초기 이온 농도 상태 (예: Na, K, Ca, Cl)
        self.Na = 0.0
        self.K = 0.0
        self.Ca = 0.0
        self.Cl = 0.0
        self.voltage = 0.0  # 막전위

    def ion_channel_open(self):
        # 이온 채널 개폐 조건 (예시)
        # Na+ 채널이 열리면 농도 증가
        self.Na += 0.1
        self.K -= 0.05
        self.Ca += 0.05
        self.Cl -= 0.02

    def update_voltage(self):
        # 간단한 전압 계산 예시
        self.voltage = self.Na - self.K + self.Ca - self.Cl

    def step(self):
        self.ion_channel_open()
        self.update_voltage()

def simulate(steps=100):
    neuron = QquartsNeuron()
    voltage_trace = []

    for _ in range(steps):
        neuron.step()
        voltage_trace.append(neuron.voltage)

    # 결과 시각화
    plt.plot(voltage_trace)
    plt.title("Qquarts Neuron Voltage Simulation")
    plt.xlabel("Time step")
    plt.ylabel("Voltage (a.u.)")
    plt.show()

if __name__ == "__main__":
    simulate()