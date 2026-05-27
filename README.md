# Study GPT

단순 질답형 챗봇이 아닌,  
사용자의 학습 흐름과 상태를 관리하는  
RAG 기반 AI Tutor Agent 프로젝트입니다.
단순한 이런 AI Agent 를 만들어 보자 라고 생각해서 만들기 보다는,
실제로 제가 자주 사용한 GPT에서 아쉬웠던 부분들, 이런 기능이 있었으면 좋겠다 라고 생각해서
실제 개발 진행 과정에 포함시켰습니다. 

---

# 프로젝트 소개

Study GPT는  
"무엇을 어떻게 공부해야 할지 모르겠다"는 문제를 해결하기 위해 제작한  
초심자 중심 AI 학습 서비스입니다.

사용자가 학습 주제를 입력하면:

- AI가 학습 의도를 분석하고
- 단계별 커리큘럼을 생성하며
- 현재 학습 상태를 기억하고
- 이어서 학습 / 복습 / 심화 설명 / 질문 응답을 제공하는

AI Tutor 형태의 학습 시스템입니다.

또한 PDF 문서를 업로드하면,
문서 기반 RAG 학습 시스템을 통해
교재처럼 단계별 학습도 가능합니다.

---

# 핵심 기능

## AI 커리큘럼 생성
- 사용자의 학습 요청 분석
- 학습 수준(초급/중급/고급) 판단
- 단계별(step) 커리큘럼 자동 생성

예시:
- "파이썬 배우고 싶어"
- "React 기초 공부하고 싶어"

↓

AI가:
- 변수
- 함수
- 배열
- 이벤트
- 컴포넌트 구조

등 단계별 학습 흐름 생성

---

## 🧠 AI Tutor 강의 시스템
- step 기반 AI 강의 생성
- 현재 학습 단계 기억
- 이어서 학습 지원
- 다시 설명 기능
- 심화 설명 기능
- 학습 중 질문 응답 기능

단순 GPT 채팅이 아니라,
실제 AI 튜터 흐름을 목표로 설계했습니다.

---

## 📄 PDF 기반 문서 학습 (RAG)

사용자가 PDF 문서를 업로드하면:

- 문서 자동 로드
- chunk 분리
- embedding 생성
- FAISS vector store 저장
- similarity search 기반 retrieval 수행

을 통해 문서 기반 질의응답 및 학습이 가능합니다.

지원 기능:
- PDF 요약
- 문서 질문 응답
- 문서 기반 단계별 학습
- 현재 step 기준 retrieval 기반 강의 생성

---

##  학습 중 질문 시스템
학습 도중:

- "이 부분 이해 안돼"
- "왜 이런 구조야?"
- "다시 설명해줘"

같은 질문이 가능하며,
현재 학습 단계 기준으로 AI가 답변합니다.

---

## 멀티 학습방 시스템
- 사용자별 여러 학습방 생성 가능
- 이전 대화 유지
- 이전 학습 상태 유지
- room 기반 메시지 관리

---

## JWT 인증 시스템
- 회원가입
- 로그인
- JWT 인증
- 사용자별 데이터 분리

---

## 학습 상태 Persistence
서버 재시작 이후에도:

- 학습 상태
- 현재 step
- curriculum
- 이전 메시지
- vector store

복구 가능하도록 설계했습니다.

---

# 🛠 기술 스택

## Backend
- FastAPI
- Python
- SQLAlchemy
- JWT Authentication

## Frontend
- React
- Tailwind CSS

## AI / LLM
- OpenAI API
- LangChain
- LangGraph
- FAISS Vector Store

## Database
- Supabase (PostgreSQL)

---

# 📂 프로젝트 구조

```bash
backend/
 ├── api/
 ├── services/
 ├── chains/
 ├── graphs/
 ├── models/
 ├── schemas/
 ├── db/
 └── main.py

frontend/
 ├── components/
 ├── pages/
 ├── services/
 └── App.jsx
 ```


## 프로젝트 설계 특징

# 1. 단순 챗봇이 아닌 "학습 흐름 기반 구조"

기존 GPT 서비스는 단발성 질답이 많지만,
Study GPT는:

curriculum, current_step, learning_status

를 기반으로 학습 흐름 자체를 관리합니다.

# 2. RAG 기반 문서 학습 시스템

PDF 문서를 단순 업로드하는 것이 아니라:

chunk 분리, embedding, vector search, retrieval

기반으로 문서 내용을 실제 학습 흐름에 연결했습니다.

# 3. 상태 기반 학습 구조

사용자는 이어서 학습, 다시 설명, 심화 설명, 현재 step 질문

등을 자연스럽게 이어갈 수 있습니다.

# 4. Vector Store Persistence

FAISS vector store를 디스크에 저장하여 서버 재시작 이후에도 문서 기억 유지가 가능하도록 설계했습니다.

## ⚠️ 개발 과정에서 해결한 문제들

PDF 기반 RAG 기억 문제

초기에는 서버 재시작 시 vector store가 사라지는 문제가 있었습니다.

→ FAISS local 저장/복구 구조 추가로 해결

문서 학습 품질 문제

초기에는 문서 전체 요약 수준 응답만 생성됨.

→

step 기반 retrieval
curriculum granularity 개선
prompt engineering 강화

를 통해 실제 강의 흐름 형태로 개선

멀티 채팅방 상태 충돌 문제

room_id 기준으로:

메시지
session
vector store

를 분리하여 해결

PDF OCR 한계 문제

이미지 기반 PDF는 text extraction 실패 가능성 확인.

→ OCR 또는 다른 parser 확장 가능성 고려

##  프로젝트 목표
초심자의 학습 시작 문제 해결
AI Tutor 기반 학습 흐름 구현
RAG 기반 문서 학습 시스템 구축
상태 기반 학습 구조 설계
실제 서비스 수준 AI 학습 시스템 구현

## 향후 개선 예정
OCR 기반 이미지 PDF 지원
학습 추천 시스템
사용자별 학습 분석
더 정교한 LangGraph 상태 흐름
학습 메모 시스템
AI 기반 오답 분석
배포 최적화 및 비용 최적화


## 프로젝트를 통해 배운 점

이 프로젝트를 통해 FastAPI 기반 API 설계 JWT 인증 구조 SQLAlchemy ORM
LangChain / LangGraph 구조 RAG 시스템 설계
Vector Search Prompt Engineering 상태 기반 AI 흐름 설계
AI 서비스 아키텍처 설계를 직접 경험했습니다.
또한, 이 프로젝트의 개발 기간은 약 2달정도 되는데, 정말 시행착오가 많았고, 모르는 부분들이 정말 많았습니다.
특히, 프론트엔드 UI,UX 개발 과정에서 정말 큰 어려움을 느꼈는데, 그럴 때마다 벽을 느꼈지만,
모르는 부분들은 찾아가며, AI 의 도움을 받아서, 원하는 대로 동작하게끔 지속적으로 시도했고, 상당한 시간이 걸렸지만
원하는 수준의 약 80% 정도 까지는 구현하는데 성공했습니다.
여전히 아쉬운 결과물이지만, 프론트쪽으로 거의 몰랐던 부분들을 직접 개발하며 부딪혀 가며, 문제점들을 찾아내고, 개선하고,
있으면 좋은 부분, 기능들을 아이디어를 내서 제 프론트 화면에 적용시켜 보니, 만족하지는 못하지만 그래도 나름 시도는 했구나 라고
스스로 생각하고 있습니다.

또한, 백엔드 개발을 하면서도, 다양한 어려움이 있었는데, JWT 인증 구조, 프롬프트 엔지니어링,
LangChain / LangGraph 구조, RAG 시스템 설계 등 상당한 곳에서도 직접 부딪혀가며 몰랐던 부분들을 알아가고, 찾아가면서
상당한 어려움이 있었지만, 그래도 나름 원하던 결과의 70%정도 까지는 구현에 성공했습니다.

아직 프롬프트 다듬기, 학습 모드를 사용자가 선택하는 기능, RAG 추가 기능(OCR 기반 이미지 PDF 지원), 학습 추천 시스템,
사용자별 학습 분석 , 더 정교한 LangGraph 상태 연결, 등 구현해야할 부분들이 많이 있는데,

부족한 부분들을 더 다듬고 공부해서, 마저 개발해 보려고 합니다.

