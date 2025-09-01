import httpx

# 모델 리스트 (Ollama에 설치되어 있어야 함)
models = {
    "GPT": "llama3.1",
    "제미나이": "mistral-nemo",
    "그록": "qwen2.5"
}

def ask_model(model_name, question):
    try:
        r = httpx.post(
            f"http://localhost:11434/api/generate",
            json={"model": model_name, "prompt": question, "stream": False},
            timeout=60
        )
        data = r.json()
        return data.get("response", "").strip()
    except Exception as e:
        return f"[에러: {e}]"

def main():
    print("=== 쿠키팜 3대장 ===")
    question = input("질문 입력: ")

    results = {}
    for label, model in models.items():
        print(f"\n--- {label} ({model}) ---")
        answer = ask_model(model, question)
        print(answer)
        results[label] = answer

    print("\n=== 종합 요약 ===")
    summary_prompt = "다음 세 답변의 공통점과 핵심 내용을 3줄로 요약해줘:\n"
    for label, text in results.items():
        summary_prompt += f"{label}: {text}\n"

    final_summary = ask_model("llama3.1", summary_prompt)
    print(final_summary)

if __name__ == "__main__":
    main()