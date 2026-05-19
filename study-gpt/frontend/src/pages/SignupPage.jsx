//SignupPage.jsx

//회원가입 화면 UI 
//회원가입 화면 + 회원가입 API 연결 담당

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { signup } from "../api/auth";

function SignupPage() {

  // 이메일 상태
  const [email, setEmail] = useState("");

  // 비밀번호 상태
  const [password, setPassword] = useState("");

  // 에러 메시지 상태
  const [error, setError] = useState("");

  // 페이지 이동 함수
  const navigate = useNavigate();


  // 회원가입 버튼 클릭 함수, 버튼 클릭시 실행
  const handleSignup = async () => {

    try {

      // 회원가입 API 요청 ,입력값 전달
      // FastAPI / singup 요청 -> 회원가입 처리
      await signup(email, password);

      // 회원가입 성공 시 로그인 페이지 이동
      navigate("/login");

    } catch (err) {

      // 회원가입 실패 메시지
      setError("회원가입에 실패했습니다.");
    }
  };


  return (
    <div className="flex items-center justify-center min-h-screen bg-zinc-950">

      <div className="w-full max-w-md p-8 bg-zinc-900 rounded-2xl shadow-lg">

        <h1 className="text-3xl font-bold text-white text-center mb-6">
          Signup
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
            onChange={(e) => setEmail(e.target.value)}
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
            className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          />
        </div>

        {/* 회원가입 버튼 */}
        <button
          onClick={handleSignup}
          className="w-full p-3 bg-white text-black rounded-lg font-semibold hover:bg-zinc-200 transition"
        >
          회원가입
        </button>

      </div>
    </div>
  );
}

export default SignupPage;