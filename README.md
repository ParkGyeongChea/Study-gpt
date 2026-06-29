
# Study GPT (MVP v1.1)

Study GPT는 단순 질답형 챗봇이 아닌,

사용자의 학습 흐름과 학습 상태를 관리하는 AI Tutor 서비스입니다.

단순히 AI Agent를 구현하는 것을 목표로 시작한 프로젝트가 아니라,

기존 GPT 서비스를 사용하며 느꼈던 학습 경험의 한계와 불편함을 개선해보고자 시작한 프로젝트입니다.

특히 기존 AI 챗봇을 사용하면서 느꼈던

- 학습 중 다른 질문을 하면 학습 흐름이 끊기는 문제
- 초보자에게 적절한 학습 순서와 커리큘럼을 제공하기 어려운 문제
- 이전 학습 내용을 이어서 학습하기 어려운 문제
- 학습 기록과 대화 맥락을 지속적으로 관리하기 어려운 문제

를 해결하는 데 초점을 두었습니다.

이를 위해 Study GPT는

- AI 기반 커리큘럼 생성
- Step 기반 학습 진행
- 학습 상태 저장 및 이어하기
- 멀티 학습방 관리
- JWT 기반 사용자 인증
- PDF/TXT 기반 문서 질의응답(RAG)
- 사이드 챗(Side Chat) 기반 보조 질문 기능

을 중심으로 설계 및 구현되었습니다.

# 프로젝트 소개

Study GPT는

"무엇을 어떻게 공부해야 할지 모르겠다"

라는 문제를 해결하기 위해 제작한 초심자 중심 AI 학습 서비스입니다.

사용자가 학습 주제를 입력하면

시스템이 학습 의도를 분석하고
적절한 커리큘럼을 생성한 뒤
현재 학습 단계(Current Step)를 기준으로 설명을 진행합니다.

또한 학습 상태를 데이터베이스에 저장하여

이어서 학습하기, 이전 학습 기록 확인, 학습방별 독립적인 진행이 가능하도록 설계하였습니다.

기존 GPT 서비스를 사용하면서 가장 아쉬웠던 점 중 하나는

학습 중 갑자기 궁금한 내용이 생겼을 때,

"이 영어 뜻이 뭐지?"
"이 코드 한 줄이 무슨 뜻이지?"
"이 개념만 잠깐 설명해줄 수 있을까?"

와 같은 질문을 하면 기존 학습 흐름이 끊어져 버린다는 점이었습니다.

이를 해결하기 위해 별도의 Side Chat 기능을 추가하였습니다.

Side Chat은 현재 학습 흐름과 별개로 동작하며,

간단한 질문을 빠르게 해결한 뒤

원래 학습하던 내용으로 자연스럽게 복귀할 수 있도록 설계하였습니다.


## 🎯 프로젝트 목표

Study GPT는 AI를 활용한 학습 과정에서 느꼈던 불편함을 해결하고, 실제로 사용하고 싶은 AI 학습 서비스를 목표로 개발한 프로젝트입니다.

개인적으로 학습 시 AI를 사용하면서, 하나의 대화 흐름 안에서만 질문이 이루어져 , 학습 흐름과의 별개의 질문이나, 학습 흐름에 해당하는 

간단한 질문(문법 등) 을 하면,  학습 흐름이 끊긴다는 느낌을 받았습니다.

이를 해결하기 위해 메인 학습 흐름을 유지하면서 추가 질문을 할 수 있는 독립적인 Side Chat 기능을 설계하고 구현했습니다.

### 주요 목표

독립적인 Side Chat을 통한 끊김 없는 학습 환경 제공

초심자가 체계적으로 학습을 시작할 수 있는 AI Tutor 구현

LangGraph 기반 상태(State) 중심 학습 흐름 설계

RAG 기반 PDF / TXT 문서 학습 시스템 구축

실제 서비스 수준의 AI 학습 플랫폼 구현


## 비로그인 사용자 정책

현재 Study GPT는 OpenAI API 비용 관리 및 서비스 안정성을 위해

로그인 사용자에게만 AI 학습 기능을 제공하고 있습니다.

비로그인 사용자는 서비스 UI와 기본 기능을 확인할 수 있으며,

실제 AI 응답, 학습 상태 저장, 채팅방 저장, 이어하기 기능은 로그인 이후 사용할 수 있습니다.

초기 설계 단계에서는 비로그인 사용자도 AI 응답을 받을 수 있도록 구현하였으나,

OpenAI API 호출 비용 관리 문제로 인해, 로그인 시에만 AI 사용이 가능하도록 설정해 두었습니다.

테스트시에, 아래에 테스트용 계정을 이용하시면 원활한 테스트가 가능합니다!



# 설치 및 실행

🌐 Live Demo

https://study-gpt-one.vercel.app/


# 테스트용 계정
테스트 시, 아래의 계정을 이용하시면 정상 이용이 가능합니다.

- email : test@naver.com
- password : 1234


### Backend

```bash
python -m venv .venv

.\.venv\Scripts\activate

python -m pip install --upgrade pip

pip install -r requirements.txt

cd study-gpt/backend

uvicorn main:app --reload
```

### Frontend

```bash
cd study-gpt/frontend

npm install

npm run dev
```

## 배포

Frontend
- Vercel

Backend
- Render

Database
- Supabase PostgreSQL

AI
- OpenAI API

## 배포 주소

Frontend (React + Vite 기반 프론트엔드 서비스)

- https://study-gpt-one.vercel.app/


Backend API (FastAPI 기반 백엔드 서버)

- https://study-gpt-backend.onrender.com/

Swagger API Docs
https://study-gpt-backend.onrender.com/docs


## 시스템 아키텍처

```text
                              User
                                │
                                ▼
              React + Vite Frontend (Vercel)
                                │
                                ▼
                 FastAPI Backend (Render)
                                │
        ┌──────────────┬──────────────┬──────────────┐
        │              │              │              │
        ▼              ▼              ▼              ▼
   Authentication   Study Agent   Side Chat      RAG Service
      (JWT)            │         (Independent)       │
        │              │              │              │
        │              ▼              ▼              ▼
        │         LangGraph       OpenAI API    PDF / TXT Upload
        │              │                             │
        │              ▼                             ▼
        │         LangChain                  OpenAI Embedding
        │              │                             │
        │              ▼                             ▼
        │         OpenAI API                FAISS Vector Store
        │              ▲                             │
        │              │                             ▼
        └──────────────┼────────────────── Similarity Search
                       │                             │
                       └─────────────── Context ─────┘
                                      │
                                      ▼
                                AI Response
                                      │
                                      ▼
                     Supabase PostgreSQL Database
                 (User / Room / Session / Message)
```


# 핵심 기능

## AI 커리큘럼 생성
- 사용자의 학습 요청 분석
- 학습 수준(초급/중급/고급) 판단
- 단계별(step) 커리큘럼 자동 생성

예시:
- "파이썬 배우고 싶어"
- "React 기초 공부하고 싶어"

↓

1. 변수
2. 함수
3. 조건문
4. 반복문
5. 자료구조

이런 식으로 단계별 학습 흐름을 생성합니다.

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

## 📄 문서 기반 학습 시스템 (RAG)

사용자가 PDF,TXT 문서를 업로드하면:

- 문서 자동 로드
- chunk 분리
- embedding 생성
- FAISS vector store 저장
- similarity search 기반 retrieval 수행

을 통해 문서 기반 질의응답 및 학습이 가능합니다.

지원 기능:
- PDF,TXT 요약
- 문서 질문 응답
- 문서 기반 단계별 학습
- 현재 step 기준 retrieval 기반 강의 생성

---

##  학습 중 질문 시스템
학습 도중:

- "이 부분 이해 안돼"
- "왜 이런 구조야?"
- "다시 설명해줘"


같은 질문이 가능하며, 현재 학습 단계(current_step)를 기준으로,  설명 흐름을 유지한 상태에서 답변을 제공합니다.

또한, 기존에 GPT 서비스를 사용하며, 있었으면 좋을것 같다고 생각한 기능인 사이드 챗을 추가하였으며,

사이드 챗 기능은 기존 채팅방의 흐름을 꺠지 않고 질문을 이어갈 수 있도록,

오른쪽에 사이드 챗 기능을 추가하여, 정말 간단한 답변(간단한 코드 뜻, 영어 뜻, 등등..) 을 입력하여,

답변을 받아볼 수 있게끔 설계하였습니다.

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
서버가 재시작된 이후에도:

- 학습 상태
- 현재 step
- curriculum
- 이전 메시지
- vector store

복구 가능하도록 설계했습니다.

---

# 🛠 기술 스택

FastAPI
SQLAlchemy
PostgreSQL(Supabase)
JWT Authentication

React
TailwindCSS

OpenAI API
LangChain
LangGraph
FAISS
---

# 📂 프로젝트 폴더 구조

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

### 문서 학습 기능 안내

현재 Study GPT의 문서 학습 기능은 PDF 및 TXT 파일 업로드를 지원합니다.

업로드된 문서는 텍스트를 추출한 뒤 벡터 데이터베이스(FAISS)에 저장되며,

이를 기반으로 문서 요약, 문서 질의응답, 문서 기반 학습 기능을 제공합니다.



### 현재 지원 범위

- PDF 파일 업로드
- TXT 파일 업로드
- 문서 요약
- 문서 기반 질의응답(RAG)
- 문서 기반 커리큘럼 생성 및 학습

### 현재 제한 사항

이미지 파일(JPG, PNG 등)은 아직 지원하지 않습니다.

스캔본 PDF 또는 이미지 기반 PDF는 OCR 기능이 적용되어 있지 않아 텍스트 추출이 제한될 수 있습니다.

긴 문서는 Retrieval 기반으로 핵심 내용을 우선 활용하므로, 전체 문서를 장문 형태로 상세 요약하는 기능은 향후 개선 예정입니다.

OpenAI API 사용량 또는 Quota 상태에 따라 응답 속도나 기능 사용에 제한이 발생할 수 있습니다.


### 향후 개선 예정

- OCR 기반 이미지 PDF 처리

- 이미지 파일(JPG, PNG) 문서 분석 지원

- DOCX, PPTX 등 추가 문서 형식 지원

- 긴 문서에 대한 다단계 요약(Multi-Step Summarization)

- 문서 기반 학습 품질 및 설명 품질 개선



## 프로젝트를 통해 배운 점


처음에는 단순히 GPT API를 호출하는 수준으로 시작했지만,
프로젝트가 커지면서 인증, 상태 관리, RAG, 벡터 저장소 관리 등
실제 서비스에서 필요한 요소들을 직접 구현해볼 수 있었습니다.

특히 학습 상태를 유지하는 구조와
문서 기반 학습 기능을 구현하면서
단순 챗봇과 서비스형 AI의 차이를 경험할 수 있었습니다.

이 프로젝트를 진행하며
FastAPI 기반 API 설계, JWT 인증 구조, SQLAlchemy ORM, LangChain / LangGraph, RAG 시스템 설계 등
다양한 기술을 직접 경험해 보았습니다.

특히 단순히 GPT API를 호출하는 수준이 아니라,
학습 상태를 관리하는 구조와 PDF 기반 문서 학습(RAG)을 구현하면서
AI 서비스의 전체 흐름을 이해할 수 있었습니다.

개발 과정에서는 JWT 인증, 상태 관리, RAG 품질 개선, 프롬프트 엔지니어링, Vector Store 저장 및 복구 등
다양한 문제를 직접 해결하며 백엔드 개발 경험을 쌓았습니다.

또한 React와 Tailwind를 활용하여 프론트엔드 UI를 직접 구현하면서,
프론트와 백엔드가 실제로 어떻게 연결되는지도 경험할 수 있었습니다.

아직 OCR 기반 문서 처리, 학습 추천 시스템, 더 정교한 LangGraph 상태 관리 등 개선할 부분이 남아있지만,
앞으로도 지속적으로 발전시켜 나갈 예정입니다.
