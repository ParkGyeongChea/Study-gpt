//LoginPage.jsx
//로그인 페이지 담당

import { useState } from "react";
import { useNavigate } from "react-router-dom";
//useNavigate = 페이지 이동 기능 

import { login } from "../api/auth";
import { saveToken } from "../utils/auth";

// 1. loginpage 화면 컴포넌트 시작

function LoginPage() { 
    //React는 화면 자체를 함수로 만든다.

  //이메일 입력값 상태 만들기, 초기값은 빈 문자열 "" 사용자가 입력한 이메일 기억하는 변수
  const [email, setEmail] = useState("");

  // 비밀번호 상태
  const [password, setPassword] = useState("");

  // 에러 메시지 상태 , 로그인 실패 메시지 저장
  const [error, setError] = useState("");

  // 페이지 이동 함수
  const navigate = useNavigate();


  // 로그인 버튼 클릭 함수 , 로그인 버튼 클릭 시 실행될 함수
  const handleLogin = async () => {

    //에러 발생 가능 코드 실행
    try {

      // 로그인 API 요청
      const result = await login(email, password);

      // access_token 저장
      saveToken(result.access_token);

      // 메인 페이지 이동
      navigate("/");

    } catch (err) {

      // 로그인 실패 시 에러 출력
      setError("이메일 또는 비밀번호가 올바르지 않습니다.");
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen bg-zinc-950">

      <div className="w-full max-w-md p-8 bg-zinc-900 rounded-2xl shadow-lg">

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
            onKeyDown={(e) => {if (e.key === "Enter"){handleLogin();}}} 
            //onKeyDown 키보드 입력시 실행되는 이벤트 , (e) 현재 눌린 키 정보 저장 객체
            //enter키 입력으로 비밀번호 입력 후 창 이동


            className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          />
        </div>

        {/* 로그인 버튼 */}
        <button
          onClick={handleLogin}
          className="w-full p-3 bg-white text-black rounded-lg font-semibold hover:bg-zinc-200 transition"
        >
          로그인
        </button>

      </div>
    </div>
  );
}

export default LoginPage;