//auth.js 

//백엔드 로그인 API 호출 담당

// /login , /signup

//로그인 요청, 회원가입 요청
//POST/login , POST/signup 같은 걸 포냄.



import axios from "axios";
//axios = 서버에 http 요청 보내는 라이브러리
//React<->FastAPI 요청 가능


// FastAPI 서버 주소
const API = axios.create({
  baseURL: "http://localhost:8000",
});


// 로그인 요청 함수 생성
export const login = async (email, password) => {
    //async (비동기함수) = 시간이 걸리는 작업을 기다릴 수 있는 함수
    // 통신, 서버 처리, db 처리 등은 시간이 걸린다. async 가 없으면 서버 응답 오기도 전에 서버가 죽을수도 있음
    //sync = 동기 , 반대의 의미 
    //JavaScript는 비동기 함수를 많이 사용한다.
    //async () => {} : 화살표 함수,(함수 짧게 쓰는 문법) 이 함수 안에서는 , {} 안의 기능 사용 가능

  const response = await API.post("/login", {
    // /login 주소로 POST 요청 보내기 , await = 서버 요청 올 떄까지 기다리기

    email,
    password,
  });

  // 즉, 다른 파일에서도 사용 가능한 login 이라는 비동기 함수를 만들고, email과 password를 받아서 처리한다는 뜻.
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