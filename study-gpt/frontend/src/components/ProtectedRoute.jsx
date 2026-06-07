//ProtectedRoute.jsx

//로그인 안 했으면 접근 막는 역할 , 보안 역할 파일
//토큰 없으면 /login 이동


import { Navigate } from "react-router-dom";
import { getToken } from "../utils/auth";


//==============================================

// 1. ProtectedRoute 리액트 컴포넌트 생성

function ProtectedRoute({ children }) { 

  const token = getToken();
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return children;
}

export default ProtectedRoute;