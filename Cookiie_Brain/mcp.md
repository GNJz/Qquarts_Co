flowchart TD

    subgraph LLM["🧠 LLM (GPT·Claude) — 대뇌 피질"]
    A1[고차원 언어·계획·추론]
    A2[목표 설정 & 전략 결정]
    end

    subgraph MCP["🟢 MCP — 척수·말초신경"]
    B1[명령 라우팅]
    B2[저지연 실시간 버스]
    B3[긴급 STOP/반사]
    end

    subgraph cookiie["⚡ cookiie (SNN) — 소뇌"]
    C1[센서 패턴 학습]
    C2[운동 제어 자동화]
    C3[강화학습 기반 보정]
    end

    subgraph Quarkka["🤖 Quarkka (ROS) — 근육·감각기관"]
    D1[모터 제어]
    D2[IMU/센서 피드백]
    D3[실시간 상태 업데이트]
    end

    %% LLM ↔ MCP
    A1 -->|자연어 명령·전략| MCP
    MCP -->|상태 요약 보고| A2

    %% MCP ↔ cookiie
    MCP -->|센서데이터 실시간 피드| cookiie
    cookiie -->|제어 보정값| MCP

    %% MCP ↔ Quarkka
    MCP -->|모터/액추에이터 제어| Quarkka
    Quarkka -->|IMU·센서 데이터| MCP

    %% 긴급 루프
    Quarkka -->|전복감지| MCP
    MCP -->|즉시 STOP| Quarkka
