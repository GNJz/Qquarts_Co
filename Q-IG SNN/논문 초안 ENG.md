# Modulation of Spiking Activity in LIF-Based Neural Networks via Threshold Control

**Jazzin Yoon**, Qquarts AI Lab, Sydney, Australia  
Email: jazzin@qig.ai

---

## Abstract
We simulate a spiking neural network (SNN) using the **Leaky Integrate-and-Fire (LIF)** neuron model to investigate the effect of **inhibitory gating (IG)** on neural firing patterns.  
Under baseline conditions (**α=1.0**), neurons exhibit limited spiking activity. When IG is activated (**α=0.7**), the firing threshold is lowered, resulting in a **4.7× increase** in total spiking activity (from 0 to 86 spikes).  
This demonstrates that **dynamic threshold control** can effectively modulate neuronal sensitivity and improve information encoding in SNN architectures.

---

### **Keywords**
Spiking Neural Networks (SNN), Leaky Integrate-and-Fire (LIF), Neural Threshold Modulation, Inhibitory Gating, Computational Neuroscience

---

## 1. Introduction

Recent advancements in **Spiking Neural Networks (SNNs)** highlight the importance of biologically inspired neural dynamics for efficient information processing.  
Unlike traditional artificial neural networks (ANNs), SNNs leverage **discrete spikes** to represent information over time, enabling **energy-efficient computation** and **event-driven encoding**.

A key mechanism controlling spiking activity is the **neuronal firing threshold**.  
- High thresholds result in fewer spikes (conservative behavior).  
- Lower thresholds increase neuron sensitivity, producing more spikes (aggressive behavior).

In this study, we investigate the effect of **threshold modulation** via an **Inhibitory Gate (IG)** on LIF-based spiking neurons. We aim to quantify the impact of IG activation on:
1. **Total spiking counts**  
2. **Temporal spike distribution**  
3. **Neuron sensitivity**

---

## 2. Methods

### 2.1 LIF Neuron Model
We use the standard **Leaky Integrate-and-Fire** neuron model, where the membrane potential \( V(t) \) evolves as:

\[
\tau \frac{dV}{dt} = -V + RI
\]

- \( \tau \): Membrane time constant  
- \( R \): Membrane resistance  
- \( I \): Input current  
- \( V \): Membrane potential

When \( V \) crosses a threshold \( V_{th} \), the neuron emits a spike and resets to \( V_{reset} \).

---

### 2.2 Experimental Setup

| Parameter               | Baseline (IG Off) | IG On | Description             |
|------------------------|------------------|-------|-------------------------|
| Simulation Time (s)    | 1.0              | 1.0   | Total runtime           |
| Time Step (Δt, ms)     | 1                | 1     | Temporal resolution     |
| Threshold \(V_{th}\)   | **1.0**          | **0.7** | Firing threshold        |
| Input Current (I)      | Constant         | Constant | External input        |
| Inhibitory Gate (IG)   | Off              | On    | Sensitivity controller |

---

## 3. Results

### 3.1 Spike Counts

| Experiment       | Total Spikes | Relative Change |
|-----------------|-------------|------------------|
| Baseline (α=1.0) | 0           | —                |
| IG On (α=0.7)    | **86**      | **+470%**        |

### 3.2 Raster Plots

<div align="center">
<img src="figs/raster_baseline.png" width="45%">  
<sub><b>Fig. 1.</b> Raster Plot — Baseline (α=1.0)</sub>

<img src="figs/raster_ig.png" width="45%">  
<sub><b>Fig. 2.</b> Raster Plot — IG On (α=0.7)</sub>
</div>

---

## 4. Discussion

The results show that **IG activation significantly enhances spiking activity**. Lowering the threshold from 1.0 to 0.7 increased sensitivity and allowed neurons to fire more frequently.

This suggests that:
- Threshold modulation could improve **information encoding density** in SNNs.
- Dynamic IG control mechanisms can be leveraged for **adaptive neural computation**.

---

## 5. Conclusion

This study demonstrates that **threshold control** via IG directly affects spiking behavior in LIF-based SNNs.  
Future work will focus on:
- Scaling the network to **hundreds of neurons**
- Testing different IG strategies
- Integrating **synaptic plasticity** (STDP) for adaptive learning.

---

## Acknowledgments
This research was conducted at **Qquarts AI Lab**, Sydney.  
All experiments were performed on local compute resources using Python 3.11.
