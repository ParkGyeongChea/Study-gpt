//auth.js 

//백엔드 로그인 API 호출 담당

// /login , /signup

//로그인 요청, 회원가입 요청
//POST/login , POST/signup 같은 걸 포냄.

import axios from "axios";


// FastAPI 서버 주소
const API = axios.create({
  baseURL: "https://study-gpt-backend.onrender.com",
});


// 로그인 요청 함수 생성
export const login = async (email, password) => {
  
  const response = await API.post("/login", {
    email,
    password,
  });

  return response.data;
};


// 회원가입 요청
export const signup = async (email, password) => {

  const response = await API.post("/signup", {
    email,
    password,
  });

  return response.data;
};