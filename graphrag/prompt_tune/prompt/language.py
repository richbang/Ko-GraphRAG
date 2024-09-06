# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""Fine-tuning prompts for language detection."""
# 언어 한국어
DETECT_LANGUAGE_PROMPT = """
당신은 텍스트 문서의 정보를 분석하는 데 도움을 주는 지능형 어시스턴트입니다.
샘플 텍스트가 주어졌을 때, 해당 텍스트의 주요 언어가 무엇인지 사용자에게 알려주세요.
예를 들어: "영어", "스페인어", "일본어", "포르투갈어" 등이 있습니다.

텍스트: {input_text}
언어:"""