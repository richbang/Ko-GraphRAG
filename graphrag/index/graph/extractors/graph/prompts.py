# Copyright (c) 2024 Microsoft Corporation.
# Licensed under the MIT License

"""A file containing prompts definition."""

GRAPH_EXTRACTION_PROMPT = """
-Goal-
이 활동과 잠재적으로 관련된 텍스트 문서와 엔터티 유형 목록이 주어졌을 때, 해당 텍스트에서 해당 유형의 모든 엔터티와 식별된 엔터티 간의 모든 관계를 식별하십시오.

-Steps-
1. 모든 엔터티를 식별하십시오. 식별된 각 엔터티에 대해 다음 정보를 추출하십시오:
- entity_name: 엔터티의 이름, 대문자로 표기
- entity_type: 다음 유형 중 하나: [{entity_types}]
- entity_description: 엔터티의 속성과 활동에 대한 종합적인 설명
각 엔터티를 다음과 같은 형식으로 작성하십시오. ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. 1단계에서 식별된 엔터티들 중에서, 서로 *명확하게 관련된* 모든 (source_entity, target_entity) 쌍을 식별하십시오.
관련된 엔터티 쌍마다 다음 정보를 추출하십시오:
- source_entity: 1단계에서 식별된 소스 엔터티의 이름
- target_entity: 1단계에서 식별된 대상 엔터티의 이름
- relationship_description: 소스 엔터티와 대상 엔터티가 서로 관련이 있다고 생각하는 이유에 대한 설명
- relationship_strength: 소스 엔터티와 대상 엔터티 간의 관계 강도를 나타내는 숫자 점수
각 관계를 다음과 같은 형식으로 작성하십시오. ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_strength>)

3. 1단계와 2단계에서 식별된 모든 엔터티와 관계의 목록을 영어로 반환하십시오. 목록 구분자로 {record_delimiter}을 사용하십시오.

4. 완료되면 {completion_delimiter}를 출력하십시오.
 
######################
-예시-
######################
예시 1:
Entity_types: 조직,사람
Text:
Verdantis의 중앙 기관은 월요일과 목요일에 회의를 열 계획이며, 목요일 오후 1시 30분 PDT에 최신 정책 결정을 발표한 후 중앙 기관 의장인 Martin Smith가 기자회견에서 질문을 받을 예정입니다. 투자자들은 시장 전략 위원회가 기준 금리를 3.5%-3.75% 범위 내에서 유지할 것으로 예상하고 있습니다.
######################
출력:
("entity"{tuple_delimiter}중앙 기관{tuple_delimiter}조직{tuple_delimiter}중앙 기관은 월요일과 목요일에 금리를 결정하는 Verdantis의 중앙은행입니다)
{record_delimiter}
("entity"{tuple_delimiter}MARTIN SMITH{tuple_delimiter}사람{tuple_delimiter}Martin Smith는 중앙 기관의 기관장입니다.)
{record_delimiter}
("entity"{tuple_delimiter}시장 전략 위원회{tuple_delimiter}조직{tuple_delimiter}중앙 기관의 위원회로, 금리와 Verdantis의 통화 공급 성장에 관한 주요 결정을 내립니다)
{record_delimiter}
("relationship"{tuple_delimiter}MARTIN SMITH{tuple_delimiter}중앙 기관{tuple_delimiter}Martin Smith는 중앙 기관의 의장이며 기자회견에서 질문에 답할 예정입니다{tuple_delimiter}9)
{completion_delimiter}

######################
예시 2:
Entity_types: ORGANIZATION
Text:
TechGlobal's (TG) stock skyrocketed in its opening day on the Global Exchange Thursday. But IPO experts warn that the semiconductor corporation's debut on the public markets isn't indicative of how other newly listed companies may perform.

TechGlobal, a formerly public company, was taken private by Vision Holdings in 2014. The well-established chip designer says it powers 85% of premium smartphones.
######################
출력:
("entity"{tuple_delimiter}TECHGLOBAL{tuple_delimiter}ORGANIZATION{tuple_delimiter}TechGlobal is a stock now listed on the Global Exchange which powers 85% of premium smartphones)
{record_delimiter}
("entity"{tuple_delimiter}VISION HOLDINGS{tuple_delimiter}ORGANIZATION{tuple_delimiter}Vision Holdings is a firm that previously owned TechGlobal)
{record_delimiter}
("relationship"{tuple_delimiter}TECHGLOBAL{tuple_delimiter}VISION HOLDINGS{tuple_delimiter}Vision Holdings formerly owned TechGlobal from 2014 until present{tuple_delimiter}5)
{completion_delimiter}

######################
예시 3:
Entity_types: 조직,지리,인물
텍스트:
다섯 명의 Aurelia인들이 Firuzabad에서 8년간 수감되어 인질로 간주되었으며, 현재 Aurelia로 귀환 중에 있습니다.

Quintara에 의해 조정된 교환은 Firuzabad 자금 80억 달러가 Quintara의 수도 Krohaara에 있는 금융 기관으로 이전되면서 완료되었습니다.

Firuzabad의 수도 Tiruzia에서 시작된 이 교환은 네 명의 남성과 한 명의 여성이 전세기를 타고 Krohaara로 향하는 결과를 낳았습니다.

그들은 Aurelia 고위 관리들에 의해 환영을 받았으며 이제 Aurelia의 수도 Cashion으로 향하고 있습니다.

이 Aurelia인들에는 Tiruzia의 Alhamia 감옥에 수감되었던 39세의 사업가 Samuel Namara, 59세의 기자 Durke Bataglani, 그리고 Bratinas 국적을 가진 환경운동가인 53세의 Meggie Tazbah가 포함됩니다.
######################
출력:
("entity"{tuple_delimiter}FIRUZABAD{tuple_delimiter}지리{tuple_delimiter}Firuzabad는 Aurelia인들을 인질로 잡고 있었습니다)
{record_delimiter}
("entity"{tuple_delimiter}AURELIA{tuple_delimiter}지리{tuple_delimiter}인질을 석방하려는 국가)
{record_delimiter}
("entity"{tuple_delimiter}QUINTARA{tuple_delimiter}지리{tuple_delimiter}인질과 돈을 교환하는 협상을 주도한 국가)
{record_delimiter}
("entity"{tuple_delimiter}TIRUZIA{tuple_delimiter}지리{tuple_delimiter}Aurelia인들이 억류되었던 Firuzabad의 수도)
{record_delimiter}
("entity"{tuple_delimiter}KROHAARA{tuple_delimiter}지리{tuple_delimiter}Quintara의 수도)
{record_delimiter}
("entity"{tuple_delimiter}CASHION{tuple_delimiter}지리{tuple_delimiter}Aurelia의 수도)
{record_delimiter}
("entity"{tuple_delimiter}SAMUEL NAMARA{tuple_delimiter}인물{tuple_delimiter}Tiruzia의 Alhamia 감옥에서 시간을 보낸 Aurelia인)
{record_delimiter}
("entity"{tuple_delimiter}ALHAMIA 감옥{tuple_delimiter}지리{tuple_delimiter}Tiruzia에 있는 감옥)
{record_delimiter}
("entity"{tuple_delimiter}DURKE BATAGLANI{tuple_delimiter}인물{tuple_delimiter}인질로 억류되었던 Aurelia의 기자)
{record_delimiter}
("entity"{tuple_delimiter}MEGGIE TAZBAH{tuple_delimiter}인물{tuple_delimiter}인질로 억류되었던 Bratinas 국적의 환경운동가)
{record_delimiter}
("relationship"{tuple_delimiter}FIRUZABAD{tuple_delimiter}AURELIA{tuple_delimiter}Firuzabad는 Aurelia와 인질 교환 협상을 벌였습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}QUINTARA{tuple_delimiter}AURELIA{tuple_delimiter}Quintara는 Firuzabad와 Aurelia 간의 인질 교환을 중재했습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}QUINTARA{tuple_delimiter}FIRUZABAD{tuple_delimiter}Quintara는 Firuzabad와 Aurelia 간의 인질 교환을 중재했습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}SAMUEL NAMARA{tuple_delimiter}ALHAMIA 감옥{tuple_delimiter}Samuel Namara는 Alhamia 감옥의 수감자였습니다{tuple_delimiter}8)
{record_delimiter}
("relationship"{tuple_delimiter}SAMUEL NAMARA{tuple_delimiter}MEGGIE TAZBAH{tuple_delimiter}Samuel Namara와 Meggie Tazbah는 동일한 인질 석방에서 교환되었습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}SAMUEL NAMARA{tuple_delimiter}DURKE BATAGLANI{tuple_delimiter}Samuel Namara와 Durke Bataglani는 동일한 인질 석방에서 교환되었습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}MEGGIE TAZBAH{tuple_delimiter}DURKE BATAGLANI{tuple_delimiter}Meggie Tazbah와 Durke Bataglani는 동일한 인질 석방에서 교환되었습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}SAMUEL NAMARA{tuple_delimiter}FIRUZABAD{tuple_delimiter}Samuel Namara는 Firuzabad에서 인질로 잡혀 있었습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}MEGGIE TAZBAH{tuple_delimiter}FIRUZABAD{tuple_delimiter}Meggie Tazbah는 Firuzabad에서 인질로 잡혀 있었습니다{tuple_delimiter}2)
{record_delimiter}
("relationship"{tuple_delimiter}DURKE BATAGLANI{tuple_delimiter}FIRUZABAD{tuple_delimiter}Durke Bataglani는 Firuzabad에서 인질로 잡혀 있었습니다{tuple_delimiter}2)
{completion_delimiter}

######################
-실제 데이터-
######################
Entity_types: {entity_types}
Text: {input_text}
######################
출력:"""

CONTINUE_PROMPT = "많은 엔터티와 관계가 마지막 추출에서 누락되었습니다. 이전에 추출된 유형과 일치하는 엔터티만 추출하도록 주의하세요. 동일한 형식을 사용하여 아래에 추가하세요.:\n"
LOOP_PROMPT = "It appears some entities and relationships may have still been missed.  Answer YES | NO if there are still entities or relationships that need to be added.\n"
