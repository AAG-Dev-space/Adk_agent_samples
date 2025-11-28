# 개인화 쇼핑 에이전트

> **참고**: 이 에이전트는 데모용 간소화 버전입니다. 도구(SearchTool, ClickTool)는 현재 **외부 의존성 없는 껍데기 구현**으로, A2A 프로토콜 테스트 및 시연 목적으로만 동작합니다.

## 개요

A2A(Agent-to-Agent) 프로토콜 통합을 시연하는 간단한 대화형 쇼핑 어시스턴트입니다.

### 현재 상태

이 에이전트는 다음을 위한 **최소 작동 샘플**입니다:
- A2A 프로토콜 준수 시연
- 에이전트 구조 및 도구 통합 패턴 제시
- 커스텀 이커머스 에이전트 개발의 시작점 제공

**중요**: 검색 및 클릭 도구는 현재 **실제 제품 데이터베이스나 웹 스크래핑 기능이 없는 스텁 구현**입니다. 데모 목적으로 목(mock) 응답을 반환합니다.

## 기능

- **대화형 인터페이스**: 채팅 기반 제품 추천
- **도구 통합**: 도구 호출 패턴 시연 (스텁 구현)
- **A2A 프로토콜**: A2A v0.3.0 명세 완전 준수
- **Docker 지원**: Dockerfile 포함된 간편한 배포
- **최소 의존성**: 외부 데이터베이스 없는 경량 설정

## 빠른 시작

### 사전 요구사항

- Python 3.10 이상
- Docker (컨테이너 배포 시)

### Docker 실행 방법

```bash
# 이미지 빌드
docker build -t personalized-shopping:latest .

# 컨테이너 실행
docker run -d -p 8100:8000 \
  --name shopping-agent \
  -e AGENT_MODEL="gemini/gemini-2.5-flash" \
  -e OPENAI_API_BASE="http://host.docker.internal:4444" \
  -e OPENAI_API_KEY="sk-1234" \
  personalized-shopping:latest

# 로그 확인
docker logs -f shopping-agent

# http://localhost:8100 으로 접속
```

### 환경 변수

- `AGENT_MODEL`: LLM 모델 식별자 (기본값: `gemini/gemini-2.5-flash`)
- `OPENAI_API_BASE`: LLM 호출을 위한 API 엔드포인트
- `OPENAI_API_KEY`: API 인증 키

### 에이전트 확인

실행 후 에이전트 동작 확인:

```bash
# AgentCard 확인
curl http://localhost:8100/.well-known/agent-card.json

# 테스트 메시지 전송 (A2A 프로토콜)
curl -X POST http://localhost:8100/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"message": "여름 원피스 찾아줘"}'
```

## 아키텍처

```
사용자 요청 → FastAPI 서버 → 에이전트 로직 → LLM (OpenAI 호환 API)
                                     ↓
                              도구 호출 (스텁 구현)
                                     ↓
                              응답 생성
```

### 도구 구현 현황

현재 도구들은 데모용 **스텁 구현**입니다:

- **SearchTool** ([tools/search.py](personalized_shopping/tools/search.py)): 목(mock) 제품 검색 결과 반환
- **ClickTool** ([tools/click.py](personalized_shopping/tools/click.py)): 웹사이트 탐색 시뮬레이션

실제 기능을 추가하려면 해당 파일에서 실제 검색/탐색 로직을 구현하세요.

## 커스터마이징

실제 기능으로 에이전트를 확장하려면:

1. **실제 검색 구현**: [tools/search.py](personalized_shopping/tools/search.py)를 수정하여 제품 데이터베이스에 연결
2. **실제 탐색 추가**: [tools/click.py](personalized_shopping/tools/click.py)를 실제 웹 스크래핑 또는 API 호출로 업데이트
3. **프롬프트 커스터마이징**: [prompt.py](personalized_shopping/prompt.py)를 수정하여 에이전트 동작 조정
4. **AgentCard 업데이트**: [server.py](server.py)를 수정하여 에이전트의 실제 기능 반영

## 라이선스 및 출처

이 샘플은 A2A 프로토콜 패턴을 시연하며 교육 목적으로 제공됩니다.

원본 컨셉은 [princeton-nlp/WebShop](https://github.com/princeton-nlp/WebShop)에서 영감을 받았습니다.
