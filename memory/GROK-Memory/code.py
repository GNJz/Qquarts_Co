import numpy as np
import pandas as pd
from scipy.integrate import odeint
import matplotlib.pyplot as plt


class PlanariaLab:
    def __init__(self):
        self.experiments = {}
        self.count = 0

    def run_three_body_simulation(self, params):
        G, m1, m2, m3, t_max, dt = params
        t = np.arange(0, t_max, dt)

        # 초기 상태 [x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3]
        initial_state = [0, 0, 0, 0,
                         1, 0, 0, 0.5,
                         -1, 0, 0, -0.5]

        def three_body(state, t, G, m1, m2, m3):
            x1, y1, vx1, vy1, x2, y2, vx2, vy2, x3, y3, vx3, vy3 = state

            # 거리 계산
            r12 = np.sqrt((x2 - x1)**2 + (y2 - y1)**2 + 1e-6)
            r13 = np.sqrt((x3 - x1)**2 + (y3 - y1)**2 + 1e-6)
            r23 = np.sqrt((x3 - x2)**2 + (y3 - y2)**2 + 1e-6)

            # 가속도 계산
            ax1 = G*m2*(x2-x1)/r12**3 + G*m3*(x3-x1)/r13**3
            ay1 = G*m2*(y2-y1)/r12**3 + G*m3*(y3-y1)/r13**3
            ax2 = G*m1*(x1-x2)/r12**3 + G*m3*(x3-x2)/r23**3
            ay2 = G*m1*(y1-y2)/r12**3 + G*m3*(y3-y2)/r23**3
            ax3 = G*m1*(x1-x3)/r13**3 + G*m2*(x2-x3)/r23**3
            ay3 = G*m1*(y1-y3)/r13**3 + G*m2*(y2-y3)/r23**3

            return [vx1, vy1, ax1, ay1,
                    vx2, vy2, ax2, ay2,
                    vx3, vy3, ax3, ay3]

        sol = odeint(three_body, initial_state, t, args=(G, m1, m2, m3))

        df = pd.DataFrame({
            'Time': t,
            'x1': sol[:, 0], 'y1': sol[:, 1],
            'x2': sol[:, 4], 'y2': sol[:, 5],
            'x3': sol[:, 8], 'y3': sol[:, 9]
        })

        self.experiments[f'ThreeBody_{self.count}'] = df
        self.count += 1
        return df

    def save_data(self, filename='planaria_threebody.csv'):
        pd.concat(
            self.experiments.values(),
            keys=self.experiments.keys()
        ).to_csv(filename)
        print(f"Data saved to {filename}")

    def plot_three_body(self, exp_key):
        df = self.experiments[exp_key]
        plt.figure(figsize=(6, 6))
        plt.plot(df['x1'], df['y1'], label='Body 1')
        plt.plot(df['x2'], df['y2'], label='Body 2')
        plt.plot(df['x3'], df['y3'], label='Body 3')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('2D Three-Body Problem Simulation')
        plt.legend()
        plt.savefig(f'figures/{exp_key}.png', dpi=150)
        plt.show()


# 실행부
if __name__ == "__main__":
    lab = PlanariaLab()
    params = (1.0, 1.0, 1.0, 1.0, 10.0, 0.01)
    df = lab.run_three_body_simulation(params)
    lab.save_data()
    lab.plot_three_body('ThreeBody_0')
