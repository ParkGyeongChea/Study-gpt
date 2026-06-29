//api.js
//백엔드 API 요청 전용 파일 (로그인,Room 조회, 메시지 조회, AI 요청 전부 여기서 처리)

//==================================================

//백엔드 API 통신 전용 파일 axios 라이브러리 가져오기
import axios from "axios";

// 1.api 객체 생성 , axios 설정 묶음 객체 생성.(api.get ,api.post 형태로 사용 가능)
const api = axios.create({

    //1. 서버의 기본 주소 설정 (백엔드<->프론트 연결 핵심 코드)
    baseURL:"https://study-gpt-backend.onrender.com",
    // baseURL:"http://127.0.0.1:8000",

    headers: { //headers 설정 (JSON 형식으로 데이터 보낸다고 서버에 알림)
        "Content-Type": "application/json",
    },
});


// 2. 요청 보내기 전에 자동 실행
api.interceptors.request.use(
  (config) => {

    // localStorage에 저장된 access_token 가져오기
    const token = localStorage.getItem("token");

    // 토큰 존재하면 Authorization 헤더 추가
    if (token) {

      config.headers.Authorization = `Bearer ${token}`;
      // backend JWT 인증용 헤더 추가
    }
    return config;
  }

);


export default api;






