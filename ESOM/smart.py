# 맛 시뮬레이터: 5가지 맛 이퀄라이저 조정

class TasteEQ:
    def __init__(self):
        self.tastes = {
            'sweet': 0,
            'salty': 0,
            'sour': 0,
            'bitter': 0,
            'umami': 0
        }

    def set_taste(self, taste, level):
        if taste in self.tastes:
            self.tastes[taste] = max(0, min(level, 10))  # 0~10 범위 제한

    def get_profile(self):
        return self.tastes

    def simulate_output(self):
        output = "👅 Taste Output:\n"
        for t, level in self.tastes.items():
            bar = '■' * level + '-' * (10 - level)
            output += f"{t.capitalize():7}: {bar} ({level})\n"
        return output

# 사용 예시
if __name__ == "__main__":
    eq = TasteEQ()
    eq.set_taste('sweet', 7)
    eq.set_taste('sour', 3)
    eq.set_taste('bitter', 1)
    print(eq.simulate_output())