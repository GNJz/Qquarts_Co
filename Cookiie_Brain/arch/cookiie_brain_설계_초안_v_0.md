# Cookiie Brain – 설계 초안 v0.1

> 목적: **감정·맥락 인지형 초경량 SNN**(Qquarts 4이온 + DTG-LIF)으로, 실시간 신호(텍스트/오디오/EEG 등)에서 감정/상태를 추정하고 제어 시그널을 생성.

---

## 1) 목표 & 범위

- **MVP 목표(주간)**: 텍스트 입력 → 감정 6클래스(±중립) 분류, 실시간 30FPS 이상, 노트북 CPU에서도 동작.
- **확장 목표(월간)**: 오디오, 간이 EEG(α/β/θ 밴드), 멀티모달 late fusion.
- **제약**: 파라미터 ≤ 1M, 메모리 ≤ 50MB, 추론 지연 ≤ 30ms/문장.

---

## 2) 수학 기반 (핵심 3식)

1. **DTG-LIF(동적 임계값)**\
   \(\;V_{\mathrm{th}}(t)=V_0+\alpha E(t)-\beta I(t)\;\)
2. **카오스/안정(품질 관리용)**\
   \(\;\lambda=\lim_{t\to\infty}\frac{1}{t}\ln\frac{\Delta x(t)}{\Delta x(0)}\;\)\n   → 훈련/추론 중 **발화 다이내믹스 안정성 점검** 지표로 사용.
3. **Qquarts 4이온 막전위**\
   \(\;\Delta V=\sum_{i\in\{Na,K,Ca,Cl\}}g_i\,(E_i-V)\;\)\n   → 뉴런 state update에 **생물영감 가중**(감정 게이팅)으로 사용.

---

## 3) 시스템 아키텍처

```mermaid
flowchart LR
  TXT[텍스트 입력] --> |토큰/임베딩| FE[전처리/피처]
  AUD[오디오 입력] --> |MFCC/Spec| FE
  EEG[EEG αβθ]|옵션| --> |밴드전력| FE
  FE --> GATE[Emotion Gate (4-ion)]
  GATE --> SNN[DTG-LIF Spiking Layer(s)]
  SNN --> READ[Readout (線形+Softmax)]
  READ --> OUT{감정/상태}
  OUT --> CTRL[제어신호/피드백]
```

- **Emotion Gate**: 4이온 전도도 \(g_i\)를 감정 priors로 미세 조정 → DTG-LIF 입력 \(E/I\)에 가중.
- **DTG-LIF 층**: 스파이크율로 특징 추출 → 저전력/저파라미터.
- **Readout**: 선형/로지스틱 계열. 추후 양자화(HW 친화).

---

## 4) 데이터 & 레이블링

- **텍스트**: 감정 레이블(긍/부/분노/슬픔/두려움/놀람/중립), 문장 길이 ≤ 128 토큰.
- **오디오(확장)**: 16kHz, 1–3초 클립, MFCC 40ch.
- **EEG(확장)**: 밴드 전력(α,β,θ), 250Hz → 10Hz 리샘플.

전처리 파이프라인:

```mermaid
flowchart LR
  RAW[원천 데이터]-->CLEAN[정제/필터]
  CLEAN-->AUG[증강(옵션)]
  AUG-->SPLIT[Train/Val/Test]
  SPLIT-->FEATURE[임베딩/특징]
  FEATURE-->CACHE[(Feature Cache)]
```

---

## 5) 모듈 구성(제안 디렉터리)

```
Qquarts_Co/
└─ core/
   └─ cookie_brain/
      ├─ __init__.py
      ├─ dtg_lif.py              # DTG-LIF 뉴런/레이어
      ├─ ion_gate.py             # 4-ion 게이트(감정 priors)
      ├─ encoder_text.py         # 텍스트 임베딩(mini)
      ├─ encoder_audio.py        # 오디오 특징(MFCC)
      ├─ head_readout.py         # readout 레이어
      ├─ pipeline_train.py       # 훈련 루틴
      ├─ pipeline_infer.py       # 실시간 추론
      ├─ metrics.py              # f1, cali., stability(λ proxy)
      ├─ config.yaml             # 설정 템플릿
      └─ examples/
         ├─ demo_infer.py
         └─ sample_inputs.txt
```

> *주의*: **홈페이지 구조 불변**. 위 경로만 사용, 웹 관련 폴더/루트는 **접근 금지**.

---

## 6) 설정 템플릿 (config.yaml)

```yaml
model:
  snn_layers: 2
  hidden: 256
  dtg:
    V0: 1.0
    alpha: 0.8
    beta: 0.6
  ions:
    g: {Na: 0.9, K: 0.7, Ca: 0.4, Cl: 0.3}
    E: {Na: 55.0, K: -90.0, Ca: 132.0, Cl: -65.0}
train:
  batch_size: 64
  epochs: 20
  lr: 3e-4
  seed: 42
  amp: true
data:
  text_path: data/text_emotion.csv
  val_ratio: 0.1
export:
  onnx: out/cookie_brain.onnx
  quantize: int8
```

---

## 7) 훈련 루틴(의사코드)

```python
# pipeline_train.py (pseudo)
for batch in loader:
    x = encode_text(batch.text)
    e,i = gate_4ion(x)                  # 4-ion 게이팅 → (E, I)
    spikes = dtg_lif(x, E=e, I=i)       # DTG-LIF forward
    logits = readout(spikes)
    loss = ce_loss(logits, batch.label)

    loss.backward(); opt.step(); opt.zero_grad()

    # 안정성 모니터 (λ proxy)
    if step % K == 0:
        lam = lyapunov_proxy(spikes)
        assert lam < LMAX, "instability detected"
```

---

## 8) 지표 & 합격선

| 범주  | 지표         | 목표                      |
| --- | ---------- | ----------------------- |
| 정확도 | macro-F1   | **≥ 0.78** (텍스트 6+1 감정) |
| 속도  | 추론지연       | **≤ 30ms/문장** (CPU i5급) |
| 경량화 | 모델크기       | **≤ 50MB**, 파라미터 ≤ 1M   |
| 안정성 | λ-proxy    | **< 0.5** (발화 다이내믹스)    |
| 신뢰  | Calib. ECE | **≤ 0.08**              |

---

## 9) 테스트 시나리오(핵심)

1. **기본 정확도**: 공개 감정코퍼스 2개 교차검증 → macro-F1 ≥ 0.78.
2. **지연 측정**: 배치=1, CPU 추론 1,000문장 평균 ≤ 30ms.
3. **안정성**: 훈련 후 10분 추론 스트레스에서 λ-proxy < 0.5 유지.
4. **온·오프라인 동등성**: onnx/int8 모델과 PyTorch FP 모델 예측 일치율 ≥ 99%.

---

## 10) 내일 작업(우선순위 체크리스트)

-

**Stretch(되면)**

-

---

## 11) 위험요인 & 완화

- **데이터 편향**: 한국어/영어 균형 → 다국어 소량 샘플링 혼합.
- **발화 불안정**: 학습 초기에 α/β warm-up 스케줄.
- **성능 한계**: readout 앞단에 얕은 residual conv(옵션) 도입.

---

## 12) 버전닝 & 산출물

- 태그: `cookiebrain-v0.1-mvp` (MVP 완료 시)
- 산출: `out/cookie_brain.onnx`, `report/ablation.pdf`, `fig/λ-stability.png`

---

## 13) 부록: 예시 CLI

```bash
# 훈련
python -m core.cookie_brain.pipeline_train --config core/cookie_brain/config.yaml

# 추론 데모
python -m core.cookie_brain.examples.demo_infer --text "오늘 진짜 기분 최고야"

# 내보내기
python -m core.cookie_brain.export --onnx out/cookie_brain.onnx --quant int8
```

