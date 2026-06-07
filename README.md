
# Study GPT (MVP v1)

단순 질답형 챗봇이 아닌,  
사용자의 학습 흐름과 상태를 관리하는  
RAG 기반 AI Tutor Agent 프로젝트입니다.
단순한 이런 AI Agent 를 만들어 보자 라고 생각해서 만들기 보다는,
기존 GPT 서비스를 사용하며 느꼈던 한계를 개선하기 위해 시작한 프로젝트입니다.

특히,기존 GPT 서비스를 사용하면서 느꼈던

- 학습 중 다른 질문을 하면 흐름이 끊기는 문제
- 초보자에게 적절한 학습 순서를 제공하지 못하는 문제
- PDF나 문서를 교재처럼 단계별 학습하기 어려운 문제

를 해결하는 데 초점을 두었습니다.
---

## 시스템 아키텍처

Frontend (React)
↓
Backend API (FastAPI)
↓
LangChain / LangGraph
↓
OpenAI API
↓
FAISS Vector Store
↓
Supabase PostgreSQL


## 프로젝트 소개

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


# 프로젝트 설계 특징

## 1. 단순 챗봇이 아닌 "학습 흐름 기반 구조"

기존 GPT 서비스는 단발성 질답이 많지만,
Study GPT는:

curriculum, current_step, learning_status

를 기반으로 학습 흐름 자체를 관리합니다.

## 2. RAG 기반 문서 학습 시스템

PDF 문서를 단순 업로드하는 것이 아니라:

chunk 분리, embedding, vector search, retrieval

기반으로 문서 내용을 실제 학습 흐름에 연결했습니다.

## 3. 상태 기반 학습 구조

사용자는 이어서 학습, 다시 설명, 심화 설명, 현재 step 질문

등을 자연스럽게 이어갈 수 있습니다.

## 4. Vector Store Persistence

FAISS vector store를 디스크에 저장하여 서버 재시작 이후에도 문서 기억 유지가 가능하도록 설계했습니다.

# 개발 과정에서 해결한 문제들

### PDF 기반 RAG 기억 문제
- 서버 재시작 시 vector store가 사라지는 문제 발생
- FAISS local 저장/복구 구조 추가로 해결

### 문서 학습 품질 문제
- 문서 전체 요약 수준의 응답만 생성
- step 기반 retrieval
- curriculum granularity 개선
- prompt engineering 강화

### 멀티 채팅방 상태 충돌 문제
- room_id 기준으로
  - 메시지
  - session
  - vector store
  분리

## 현재 MVP 한계

PDF OCR 한계 문제
이미지 기반 PDF는 text extraction 실패 가능성 확인.

→ OCR 또는 다른 parser 확장 가능성 고려

현재 문서 학습 기능은 PDF 파일 중심으로 동작합니다.

TXT, 이미지 파일은 아직 정식 지원하지 않습니다.

이미지 기반 PDF 또는 스캔본 PDF는 OCR 기능이 없어 텍스트 추출이 제한될 수 있습니다.

긴 PDF 문서는 현재 retrieval 기반으로 핵심 내용을 요약하므로, 전체 문서를 장문으로 상세 요약하는 기능은 향후 개선 예정입니다.

OpenAI API 사용량 또는 quota 상태에 따라 AI 응답이 제한될 수 있습니다.

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

이 프로젝트를 진행하며 FastAPI 기반 API 설계, JWT 인증 구조, SQLAlchemy ORM, LangChain / LangGraph, RAG 시스템 설계 등 다양한 기술을 직접 경험할 수 있었습니다.

특히 단순히 GPT API를 호출하는 수준이 아니라, 학습 상태를 관리하는 구조와 PDF 기반 문서 학습(RAG)을 구현하면서 AI 서비스의 전체 흐름을 이해할 수 있었습니다.

개발 과정에서는 JWT 인증, 상태 관리, RAG 품질 개선, 프롬프트 엔지니어링, Vector Store 저장 및 복구 등 다양한 문제를 직접 해결하며 백엔드 개발 경험을 쌓았습니다.

또한 React와 Tailwind를 활용하여 프론트엔드 UI를 직접 구현하면서, 프론트와 백엔드가 실제로 어떻게 연결되는지도 경험할 수 있었습니다.

아직 OCR 기반 문서 처리, 학습 추천 시스템, 더 정교한 LangGraph 상태 관리 등 개선할 부분이 남아있지만, 앞으로도 지속적으로 발전시켜 나갈 예정입니다.
