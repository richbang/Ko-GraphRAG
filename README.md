# Ko-GraphRAG
👉 [GraphRAG Accelerator](https://github.com/Azure-Samples/graphrag-accelerator) <br/>
👉 [Microsoft GraphRAG 원본 프로젝트](https://github.com/microsoft/graphrag) <br/>
👉 [Microsoft Research Blog Post](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) <br/>
👉 [GraphRAG Arxiv 논문](https://arxiv.org/pdf/2404.16130)

## 개요

Ko-GraphRAG는 Microsoft의 [GraphRAG](https://github.com/microsoft/graphrag) 프로젝트를 기반으로, 한국어 데이터에 맞춰 파인튜닝하고, 로컬 환경에서 Ollama LLM을 사용할 수 있도록 수정된 버전입니다.

이 프로젝트는 대형 언어 모델(LLM)을 활용하여 비구조화된 텍스트에서 의미 있는 구조적 데이터를 추출하는 기능을 제공합니다. 특히, 한국어 데이터에 맞춘 최적화를 통해 로컬 환경에서도 효율적으로 사용할 수 있습니다.

원본 GraphRAG 프로젝트에 대한 더 자세한 내용은 [Microsoft GraphRAG 블로그 포스트](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/)에서 확인할 수 있습니다.

## 시작하기

Ko-GraphRAG를 시작하려면, 먼저 로컬 환경에서 Ollama를 설정해야 합니다. 이 프로젝트는 Ollama를 통해 LLM의 로컬 실행을 지원하며, 이를 통해 서버 의존 없이 독립적인 시스템 구축이 가능합니다.

### 설치

1. **가상 환경을 설치하세요.**
```bash
conda create -n graphrag python=3.12
conda activate graphrag
```

2. **필요한 파일을 설치하세요.**
```bash
git clone https://github.com/richbang/Ko-GraphRAG.git
cd Ko-GraphRAG
pip install -e .
```

3. **로컬에서 Ollama를 실행해 보세요**
- 방법 1. [Ollama 홈페이지](https://ollama.com/)
- 방법 2. 다음 명령어를 터미널에서 실행하세요.
```bash
curl -fsSL https://ollama.com/install.sh | sh #ollama for linux
pip install ollama
```

4. **각 환경에 적합한 모델을 다운로드 받으세요**
본 저장소는 다음 모델들을 사용하여 GraphRAG를 실현했습니다.
1. **'mistral-nemo'**모델로 인덱싱을 수행했습니다.
2. **임베딩**모델은 **bge-m3**를 사용했습니다.
3. 인덱싱된 파일을 활용해 **추론**모델은 **llama3.1:70b**을 사용했습니다.

```bash
ollama pull mistral-nemo # 인덱싱 모델
ollama pull bge-m3 # 임베딩 모델
ollama pull llama3.1:70b # 추론 모델
```
인덱싱 모델과 추론 모델이 다른 이유는
실험에 사용된 데이터셋을 활용하기에 **mistral-nemo**모델의 성능이 충분치 않기 때문입니다.
적은 양의 데이터로는 **mistral-nemo**만으로도 충분합니다.

5. **구현 데이터셋**
본 레포의 입력 데이터셋은 뉴스 기사 기계독해 데이터로, AI Hub의 데이터를 활용했습니다.
해당 데이터셋 중에서 1000편의 기사를 무작위로 추출하여 입력 데이터로 작성했습니다.
데이터셋 출처: [AI Hub](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&dataSetSn=577)

6. **Ollama 설정**
Ollama의 모델을 **pull** 명령어로 받았을 때, 기본으로 설정된 max_token 값은 **2048**입니다.
위 GraphRAG 프로세스는 입력 데이터의 양에 따라 다르지만, 본 실험에서 입력한 1000편의 기사를 활용하기 위해 max_token을 늘릴 필요가 있습니다.
특히, 질문(Query) 과정에서 모델에 입력되는 Context 토큰의 수는 입력 데이터셋의 크기에 비례합니다.
아래는 그 max_token을 수정할 수 있는 방법입니다.
  **다운로드 받은 모델을 보는 방법**
  ```bash
  ollama list # 모델 확인
  ```

  **max_token을 수정하는 방법**
  ```bash
  ollama create 모델_이름 > Modelfile
  ```
  해당 모델의 모델파일이 생성됩니다.
  생성된 모델 파일을 열어서 적당한 위치에 다음을 추가합니다.
  **PARAMETER num_ctx 정수**
  ex) PARAMETER num_ctx 128000
  num_ctx는 max_token과 같습니다.
  수정 후 파일을 저장합니다.

  **새로운 모델 생성하기**
  ```bash
  ollama create 모델_이름 -f Modelfile
  ```
    
    권한 문제 발생시
    ```bash
    sudo chmod -R o+rx 유저폴더
    ```

7. **인덱싱 및 쿼리 방법**
  본 레포의 'test_con'폴더에는 뉴스 기사 1000편을 인덱싱한 파일이 있습니다.
  **인덱싱된 파일 활용법**
  ```bash
  python -m graphrag.query --root ./test_con --method global "질문 내용"
  ```
  메소드에는 'global' 및 'local' 두 가지가 있습니다.

  **인덱싱 폴더 초기화 방법**
  ```bash
  mkdir ./새로운_폴더
  python -m graphrag.index --init --root ./새로운_폴더
  cp ./prompts/* ./새로운_폴더/prompts
  ```
  
  프롬프트 복사를 완료한 후, 새로운 폴더 안의 settings.yaml파일을 열어 필요한 설정을 완료합니다.
  참고 설정은 'test_con/settings.yaml'을 참고하세요.

  **인덱싱 커맨드**
  ```bash
  python -m graphrag.index --root ./새로운_폴더
  ```
  위 명령어가 실행되면 초기화된 폴더 안의 'output' 디렉토리에
  폴더가 생성됩니다.(각 실행 시각의 타임 스탬프가 폴더 명임.)

8. **그래프 시각화**
  설정 파일에서
  snapshots:
    graphml: true
  를 추가하면 시각화할 수 있는 파일이 인덱싱 후 생성됩니다.
  파일은 (https://gephi.org/users/download/) 프로그램으로 열어볼 수 있습니다.
  'visualize-graphml.py'를 이용해도 마찬가지로 시각화를 할 수 있습니다.



## 프로젝트 가이드
이 저장소는 지식 그래프 메모리 구조를 활용하여 LLM의 출력을 향상시키는 방법론을 제시합니다.
Microsoft의 원본 코드를 기반으로 로컬 LLM 환경 및 한국어 데이터에 맞춰 수정되었으며, 이는 공식 Microsoft 지원 프로젝트가 아님을 밝힙니다.

⚠️ 주의: GraphRAG 인덱싱은 비용이 많이 드는 작업일 수 있습니다. 작업을 시작하기 전에 문서를 꼼꼼히 읽고, 작은 데이터셋으로 실험하는 것을 권장합니다.


## Citations

- 원본 GraphRAG 레포지토리: [GraphRAG](https://github.com/microsoft/graphrag)
- Ollama: [Ollama](https://ollama.com/)
- 'visualize-graphml.py': [graphrag-local-ollama](https://github.com/TheAiSingularity/graphrag-local-ollama)


# GraphRAG

<div align="left">
  <a href="https://pypi.org/project/graphrag/">
    <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/graphrag">
  </a>
  <a href="https://pypi.org/project/graphrag/">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/graphrag">
  </a>
  <a href="https://github.com/microsoft/graphrag/issues">
    <img alt="GitHub Issues" src="https://img.shields.io/github/issues/microsoft/graphrag">
  </a>
  <a href="https://github.com/microsoft/graphrag/discussions">
    <img alt="GitHub Discussions" src="https://img.shields.io/github/discussions/microsoft/graphrag">
  </a>
</div>

## Overview

The GraphRAG project is a data pipeline and transformation suite that is designed to extract meaningful, structured data from unstructured text using the power of LLMs.

To learn more about GraphRAG and how it can be used to enhance your LLM's ability to reason about your private data, please visit the <a href="https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/" target="_blank">Microsoft Research Blog Post.</a>

## Quickstart

To get started with the GraphRAG system we recommend trying the [Solution Accelerator](https://github.com/Azure-Samples/graphrag-accelerator) package. This provides a user-friendly end-to-end experience with Azure resources.

## Repository Guidance

This repository presents a methodology for using knowledge graph memory structures to enhance LLM outputs. Please note that the provided code serves as a demonstration and is not an officially supported Microsoft offering.

⚠️ *Warning: GraphRAG indexing can be an expensive operation, please read all of the documentation to understand the process and costs involved, and start small.*

## Diving Deeper

- To learn about our contribution guidelines, see [CONTRIBUTING.md](./CONTRIBUTING.md)
- To start developing _GraphRAG_, see [DEVELOPING.md](./DEVELOPING.md)
- Join the conversation and provide feedback in the [GitHub Discussions tab!](https://github.com/microsoft/graphrag/discussions)

## Prompt Tuning

Using _GraphRAG_ with your data out of the box may not yield the best possible results.
We strongly recommend to fine-tune your prompts following the [Prompt Tuning Guide](https://microsoft.github.io/graphrag/posts/prompt_tuning/overview/) in our documentation.

## Responsible AI FAQ

See [RAI_TRANSPARENCY.md](./RAI_TRANSPARENCY.md)

- [What is GraphRAG?](./RAI_TRANSPARENCY.md#what-is-graphrag)
- [What can GraphRAG do?](./RAI_TRANSPARENCY.md#what-can-graphrag-do)
- [What are GraphRAG’s intended use(s)?](./RAI_TRANSPARENCY.md#what-are-graphrags-intended-uses)
- [How was GraphRAG evaluated? What metrics are used to measure performance?](./RAI_TRANSPARENCY.md#how-was-graphrag-evaluated-what-metrics-are-used-to-measure-performance)
- [What are the limitations of GraphRAG? How can users minimize the impact of GraphRAG’s limitations when using the system?](./RAI_TRANSPARENCY.md#what-are-the-limitations-of-graphrag-how-can-users-minimize-the-impact-of-graphrags-limitations-when-using-the-system)
- [What operational factors and settings allow for effective and responsible use of GraphRAG?](./RAI_TRANSPARENCY.md#what-operational-factors-and-settings-allow-for-effective-and-responsible-use-of-graphrag)

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.

## Privacy

[Microsoft Privacy Statement](https://privacy.microsoft.com/en-us/privacystatement)
