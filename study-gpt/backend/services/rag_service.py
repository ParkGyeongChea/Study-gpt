# rag_service.py

# 사용자 업로드 문서 기반 RAG 처리 서비스


from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

import os

# PDF 문서 로딩 함수
def load_pdf(file_path: str):

    loader = PyPDFLoader(file_path)

    documents = loader.load()

    return documents

# TXT 문서 로딩 함수
def load_txt(file_path: str):

   
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    documents = [
        Document(page_content=text)
    ]

    return documents


# 문서를 작은 chunk로 분리하는 함수
def split_documents(documents):

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,
        chunk_overlap=200
    )

    # 문서 chunk 분리
    split_docs = text_splitter.split_documents(documents)

    return split_docs


# chunk 문서들을 vector store로 변환
def create_vector_store(split_docs):

    # OpenAI Embedding 모델 생성
    embeddings = OpenAIEmbeddings()

    # FAISS Vector Store 생성
    vector_store = FAISS.from_documents(
        split_docs,
        embeddings
    )

    return vector_store


# 사용자 질문과 관련된 문서 검색
def search_similar_documents(vector_store, query: str):

    # 유사 문서 검색 , 사용자 질문과 의미적으로 가장 가까운 chunk 검색
    docs = vector_store.similarity_search(
        query,
        k=6 
    )

    return docs


# FAISS vector_store 저장

def save_local_vector_store(vector_store,room_id: int):

    save_path = (f"vectorstores/room_{room_id}")

    os.makedirs(save_path,exist_ok=True)

    # FAISS 저장
    vector_store.save_local(save_path)
   
    print(f"VECTOR STORE 디스크 저장 완료: {save_path}")

# 저장된 FAISS 불러오기


def load_local_vector_store(room_id: int):

    load_path = (f"vectorstores/room_{room_id}")

    if not os.path.exists(load_path):

        print("저장된 VECTOR STORE 없음")

        return None

    # Embedding 모델 생성
    embeddings = OpenAIEmbeddings()

    # FAISS 로드
    vector_store = FAISS.load_local(load_path, embeddings, allow_dangerous_deserialization=True)

    print(f"VECTOR STORE 복구 완료: {load_path}")

    return vector_store


# 기존 vector_store에 새 문서 chunk 추가

def add_documents_to_vector_store(vector_store,split_docs):

    # 새 문서 chunk 추가
    vector_store.add_documents(split_docs)

    print(f"기존 VECTOR STORE 문서 추가 완료: {len(split_docs)}개")

    return vector_store