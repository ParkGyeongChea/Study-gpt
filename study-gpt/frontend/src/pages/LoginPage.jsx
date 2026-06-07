//LoginPage.jsx
//로그인 페이지 담당


import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";
import { saveToken, removeToken } from "../utils/auth";

// 1. loginpage 화면 컴포넌트 시작

function LoginPage() { 
    
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  
  const closeLoginPage = () => {
    navigate("/");
  };

  // ESC 키를 누르면 로그인 창 닫기
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") {
        closeLoginPage();
      }
    };
    window.addEventListener("keydown", handleEsc);

    return () => {
      window.removeEventListener("keydown", handleEsc);
    };
  }, []);


  // 로그인 버튼 클릭 함수 , 로그인 버튼 클릭 시 실행될 함수
  const handleLogin = async (e) => {

    console.log("로그인 함수 실행됨");

    // 브라우저 기본 form submit 방지
    if (e) {
      e.preventDefault();
    }

    console.log("try 진입 직전");

    //에러 발생 가능 코드 실행
    try {

      // 로그인 API 요청
      const result = await login(email, password);

    
      // access_token 저장
      saveToken(result.access_token);

      

      // 이메일 존재할 때만 저장
      if (result.email) {

        localStorage.setItem("email", result.email);
      }

      // 메인 페이지 이동 + 강제 새로고침
      window.location.href = "/";

    } catch (err) {
      
      console.log(err);

      // 기존 JWT 제거
      removeToken();

      // 기존 이메일 제거
      localStorage.removeItem("email");

      // 로그인 실패 메시지
      setError("이메일 또는 비밀번호가 올바르지 않습니다.");
    }
  };


  return (
    <div className="relative flex items-center justify-center min-h-screen bg-zinc-950">

      <div className="relative w-full max-w-md p-8 bg-zinc-900 rounded-2xl shadow-lg">
        {/* 로그인 창 닫기 버튼 */}
        <button
          onClick={closeLoginPage}
          className="absolute top-4 right-4 text-zinc-400 hover:text-white text-2xl leading-none transition"
        >
          ×
        </button>
        <h1 className="text-3xl font-bold text-white text-center mb-6">
          Login
        </h1>

        {/* 에러 메시지 */}
        {error && (
          <p className="text-red-500 text-sm mb-4">
            {error}
          </p>
        )}

        {/* 이메일 입력 */}
        <div className="mb-4">
          <input
            type="email"
            placeholder="이메일 입력"
            value={email}
            onChange={(e) => setEmail(e.target.value)}  // 사용자가 입력할 때마다 실행
            className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          />
        </div>

        {/* 비밀번호 입력 */}
        <div className="mb-6">
          <input
            type="password"
            placeholder="비밀번호 입력"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => {if (e.key === "Enter"){handleLogin(e);}}} 
            //onKeyDown 키보드 입력시 실행되는 이벤트 , (e) 현재 눌린 키 정보 저장 객체
            //enter키 입력으로 비밀번호 입력 후 창 이동


            className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          />
        </div>

        {/* 로그인 버튼 */}
        <button
          type="button"
          onClick={(e) => handleLogin(e)}
          className="w-full p-3 bg-white text-black rounded-lg font-semibold hover:bg-zinc-200 transition"
        >
          로그인
        </button>

      </div>
    </div>
  );
}

export default LoginPage;