//ProtectedRoute.jsx

//로그인 안 했으면 접근 막는 역할 , 보안 역할 파일

//토큰 없으면 /login 이동



import { Navigate } from "react-router-dom";
//react-router-dom 라이브러리에서 navigate 기능을 가져옴
//navigate = 강제로 다른 페이지로 보내는 컴포넌트

import { getToken } from "../utils/auth";
//utils/auth.js 파일에서 getToken 함수를 가져오는 코드.
//localStroage 안에 저장된 토큰을 꺼냄

//==============================================

// 1. ProtectedRoute 리액트 컴포넌트 생성

// 내 안에 들어온 화면을 보여줄지 말지 검사하는 컴포넌트

function ProtectedRoute({ children }) { //children =  이 컴포넌트 안에 들어온 화면을 의미

  const token = getToken();
  // localStorage 에 저장된 토큰 가져오기

  // 토큰이 없으면 로그인 페이지로 이동 , ! 는 아니다 없다 라는 뜻
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // 토큰 있으면 원래 페이지 보여주기
  return children;
}

export default ProtectedRoute;