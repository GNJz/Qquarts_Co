# 🧠 Spiking Neural Network 실험 (LIF 모델)
> 억제 게이트(Inhibitory Gate, IG) 여부에 따른 뉴런 발화 패턴 분석

## 실험 요약
| 상태 | α (Threshold) | 스파이크 개수 |
|------|---------------|---------------|
| Baseline | 1.0 | 0 |
| IG On | 0.7 | 86 |

## 결과 시각화
![Baseline](figs/raster_baseline.png)
![IG On](figs/raster_ig.png)

## 실행 방법
```bash
conda activate qig
python lif_single.py
python lif_network.py
