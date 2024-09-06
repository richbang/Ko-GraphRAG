# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A file containing prompts definition."""

CLAIM_EXTRACTION_PROMPT = """
-대상 활동-
당신은 문서에 제시된 특정 주체에 대한 주장을 분석하는 데 도움을 주는 지능형 도우미입니다.

-목표-
잠재적으로 이 활동과 관련된 텍스트 문서, 주체 명세, 주장 설명이 주어지면, 해당 주체 명세에 맞는 모든 주체와 해당 주체에 대한 모든 주장을 추출합니다.

-단계-
사전 정의된 주체 명세와 일치하는 모든 명명된 주체를 추출합니다. 주체 명세는 주체 이름 목록이거나 주체 유형 목록일 수 있습니다.
1단계에서 식별된 각 주체에 대해 주체와 관련된 모든 주장을 추출합니다. 주장은 지정된 주장 설명과 일치해야 하며, 주체가 주장에 기술된 행위의 주체여야 합니다. 각 주장을 위해 다음 정보를 추출합니다:
주체(Subject): 주장의 대상이 되는 주체의 이름을 대문자로 표기합니다. 주체는 1단계에서 식별된 명명된 주체 중 하나여야 합니다.
객체(Object): 주장에서 보고/처리하거나 행위의 영향을 받는 주체의 이름을 대문자로 표기합니다. 객체 주체가 알 수 없는 경우 NONE을 사용합니다.
주장 유형(Claim Type): 주장의 전체 카테고리를 대문자로 표기합니다. 비슷한 주장을 여러 텍스트 입력에서 반복해서 사용할 수 있도록 명명합니다.
주장 상태(Claim Status): TRUE, FALSE, 또는 SUSPECTED 중 하나를 사용합니다. TRUE는 주장이 확인된 경우, FALSE는 주장이 거짓으로 판명된 경우, SUSPECTED는 주장이 확인되지 않은 경우를 나타냅니다.
주장 설명(Claim Description): 주장의 근거와 관련 증거 및 참고 자료를 함께 설명하는 자세한 설명을 작성합니다.
주장 날짜(Claim Date): 주장이 제기된 기간(start_date, end_date)을 ISO-8601 형식으로 작성합니다. 주장이 특정 날짜에 제기되었을 경우, 동일한 날짜를 start_date와 end_date로 설정합니다. 날짜가 알려지지 않은 경우 NONE을 반환합니다.
주장 출처 텍스트(Claim Source Text): 주장의 관련된 원문 텍스트에서 모든 인용문을 나열합니다.
각 주장을 다음 형식으로 작성합니다: (<subject_entity>{tuple_delimiter}<object_entity>{tuple_delimiter}<claim_type>{tuple_delimiter}<claim_status>{tuple_delimiter}<claim_start_date>{tuple_delimiter}<claim_end_date>{tuple_delimiter}<claim_description>{tuple_delimiter}<claim_source>)

1단계와 2단계에서 식별된 모든 주장의 리스트를 **{record_delimiter}**을 목록 구분 기호로 사용하여 반환합니다.

완료 시, {completion_delimiter}을 출력합니다.

-예시-
예시 1:

주체 명세: 조직(organization)
주장 설명: 주체와 관련된 적색 신호(red flags)
텍스트: 2022년 1월 10일에 게재된 기사에 따르면, 회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다. 이 회사는 2015년에 부패 활동에 연루되었다고 의심받은 인물 C가 소유하고 있습니다.
출력:
(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022년 1월 10일에 게재된 기사에 따르면, 회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다{tuple_delimiter}2022년 1월 10일에 게재된 기사에 따르면, 회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다.) {completion_delimiter}

예시 2:

주체 명세: 회사 A, 인물 C
주장 설명: 주체와 관련된 적색 신호(red flags)
텍스트: 2022년 1월 10일에 게재된 기사에 따르면, 회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다. 이 회사는 2015년에 부패 활동에 연루되었다고 의심받은 인물 C가 소유하고 있습니다.
출력:
(COMPANY A{tuple_delimiter}GOVERNMENT AGENCY B{tuple_delimiter}ANTI-COMPETITIVE PRACTICES{tuple_delimiter}TRUE{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}2022-01-10T00:00:00{tuple_delimiter}회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다{tuple_delimiter}2022년 1월 10일에 게재된 기사에 따르면, 회사 A는 정부 기관 B가 발행한 여러 공공 입찰에 참여하는 과정에서 담합 혐의로 벌금을 부과받았습니다.) {record_delimiter} (PERSON C{tuple_delimiter}NONE{tuple_delimiter}CORRUPTION{tuple_delimiter}SUSPECTED{tuple_delimiter}2015-01-01T00:00:00{tuple_delimiter}2015-12-30T00:00:00{tuple_delimiter}2015년에 부패 활동에 연루되었다고 의심받은 인물 C{tuple_delimiter}이 회사는 2015년에 부패 활동에 연루되었다고 의심받은 인물 C가 소유하고 있습니다.) {completion_delimiter}

-실제 데이터-
다음 입력을 사용하여 응답하세요.

주체 명세: {entity_specs}
주장 설명: {claim_description}
텍스트: {input_text}
출력:"""


CONTINUE_PROMPT = "MANY entities were missed in the last extraction.  Add them below using the same format:\n"
LOOP_PROMPT = "It appears some entities may have still been missed.  Answer YES {tuple_delimiter} NO if there are still entities that need to be added.\n"
