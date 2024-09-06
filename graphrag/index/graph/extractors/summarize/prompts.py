# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A file containing prompts definition."""

SUMMARIZE_PROMPT = """
당신은 아래 제공된 데이터를 바탕으로 종합적인 요약을 생성하는 데 도움을 주는 어시스턴트입니다.
하나 또는 두 개의 엔터티와 해당 엔터티나 엔터티 그룹과 관련된 설명 목록이 주어집니다.
이 모든 설명을 하나의 종합적인 설명으로 연결하세요. 모든 설명에서 수집된 정보를 반드시 포함해야 합니다.
설명 간에 모순이 있을 경우, 모순을 해결하고 하나의 일관된 요약을 제공하세요.
3인칭으로 작성하고, 전체 문맥을 파악할 수 있도록 엔터티 이름을 반드시 포함하세요.

#######
-데이터-
엔터티: {entity_name}
설명 목록: {description_list}
#######
출력:
"""
