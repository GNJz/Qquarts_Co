
# 이온 상태 정의
ION_STATES = {
    'Cl': -1,  # 염소 - 억제
    'K': 0,    # 칼륨 - 안정화
    'Na': 1,   # 나트륨 - 신호 발생
    'Ca': 2    # 칼슘 - 신호 증폭
}

class QquartsNeuron:
    def __init__(self):
        self.state = ION_STATES['K']  # 초기 안정화 상태
        self.history = []  # 상태 기록

    def activate(self):
        self.state = ION_STATES['Na']  # 신호 발생

    def amplify(self):
        self.state = ION_STATES['Ca']  # 신호 증폭

    def inhibit(self):
        self.state = ION_STATES['Cl']  # 신호 억제

    def stabilize(self):
        self.state = ION_STATES['K']  # 안정화

    def step(self, input_signal=None):
        # 입력에 따라 상태 변화 예시
        if input_signal == 'activate':
            self.activate()
        elif input_signal == 'amplify':
            self.amplify()
        elif input_signal == 'inhibit':
            self.inhibit()
        else:
            # 자연 안정화
            self.stabilize()

        self.history.append(self.state)

class QquartsNeuralNetwork:
    def __init__(self, size):
        self.neurons = [QquartsNeuron() for _ in range(size)]
        self.size = size

    def stimulate(self, idx, signal):
        if 0 <= idx < self.size:
            self.neurons[idx].step(signal)

    def step_all(self):
        for neuron in self.neurons:
            # 여기선 간단히 안정화로 동작, 실제론 주변 뉴런 신호도 반영 가능
            neuron.step()

    def get_states(self):
        return [neuron.state for neuron in self.neurons]

# 시뮬레이션 실행 예제
if __name__ == "__main__":
    nn = QquartsNeuralNetwork(5)

    # 인덱스 2번 뉴런에 신호 발생
    nn.stimulate(2, 'activate')

    for _ in range(3):
        nn.step_all()
        print(nn.get_states())