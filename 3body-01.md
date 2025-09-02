# Three-Body Chaos & DHT-Based Hair Follicle Simulation  
> **Subtitle:** Nonlinear Dynamics, Dynamic Threshold Gating (DTG), and SNN Implications  

---

## Abstract  
본 연구에서는 **삼체 문제(Three-Body Problem)**와 **탈모(DHT 기반 모낭 밀도 감소)**를 **동적 임계값 게이트(DTG)** 관점에서 모델링하여 시뮬레이션을 수행하였다.  
삼체 문제를 통해 비선형 궤도 패턴과 카오스성을 관찰하고, 탈모 모델에서는 DHT 수준 변화가 모낭 밀도에 미치는 동적 영향을 분석했다.  
이 연구는 향후 **Spiking Neural Network(SNN)** 기반 DTG 설계에 중요한 인사이트를 제공한다.  

---

## 1. Introduction  
- **비선형 시스템 모델링**: 복잡계에서 초기 조건 민감성을 이해하기 위해 삼체 문제를 시뮬레이션.  
- **생물학적 모델링**: 탈모 원인을 DHT-DTG 상호작용으로 수학적으로 표현.  
- **목표**: 물리적 시스템(삼체 문제)과 생물학적 시스템(DHT 모델)을 통합하여 **동적 임계값 게이트(DTG)** 연구에 기여.

---

## 2. Methods  

### 2.1 Three-Body Problem (2D)  
- **수학 모델**: 뉴턴 중력 방정식 기반 ODE  
- **수치 해석**: `scipy.integrate.odeint`  
- **시각화**: Matplotlib 2D 궤도 그래프  

### 2.2 DHT-Hair Follicle Model  
- **모델 수식**:  

    \[
    \frac{dH}{dt} = rH \left(1 - \frac{H}{K}\right) - d \cdot DHT \cdot H
    \]

- `r`: 자연 성장률  
- `K`: 최대 모낭 밀도  
- `DHT`: 호르몬 수준  
- `d`: 민감도 계수  

- **의미**: DHT 수준 변화에 따른 모낭 밀도 동적 변화 모델링.

---

## 3. Results  

### 3.1 Three-Body Simulation  
- 안정된 궤도 → 준주기성  
- 초기 조건 변화 시 **카오스 패턴** 관찰  
- 시각적 데이터: `three_body_plot.png`

### 3.2 DHT-Hair Follicle Simulation  
- 정상 DHT(0.5) → 안정된 평형점 유지  
- 고 DHT(2.0) → 모낭 급격한 소실  
- 시각적 데이터: `hair_density_high.png`

---

## 4. Discussion  
- 삼체 문제의 **비선형 궤도 카오스성**과  
- DHT 기반 탈모 모델의 **동적 임계값 붕괴** 패턴은 유사한 수학적 구조를 공유.  
- SNN에서의 **Dynamic Threshold Gating(DTG)** 설계에 직간접적 인사이트 제공 가능.

---

## 5. Conclusion  
본 연구는 **삼체 문제**와 **DHT-모낭 밀도 모델**을 연계한 최초의 시뮬레이션 시도로,  
비선형 다체계에서의 동적 패턴을 SNN 설계에 적용할 가능성을 확인하였다.  

---

## 6. Files & Reproducibility  
- `src/three_body.py`
- `src/hair_simulation.py`
- `/figures/three_body_plot.png`
- `/figures/hair_density_plot.png`
