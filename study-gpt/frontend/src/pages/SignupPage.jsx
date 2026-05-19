//SignupPage.jsx

//회원가입 화면 UI 
//회원가입 화면 + 회원가입 API 연결 담당

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

//회원 가입 후 자동 로그인
import { signup, login } from "../api/auth";

import { saveToken } from "../utils/auth";

function SignupPage() {

  // 이메일 상태
  const [email, setEmail] = useState("");

  // 비밀번호 상태
  const [password, setPassword] = useState("");

  // 비밀번호 확인 입력값 상태 / setConfirmPassword = 비밀번호 재확인 입력값 저장
  const [confirmPassword, setConfirmPassword] = useState("");

  // 회원가입 성공 메시지 상태 / setSuccessMessage = 회원가입 성공 메시지 저장
  const [successMessage, setSuccessMessage] = useState("");

  // 에러 메시지 상태
  const [error, setError] = useState("");

  // 페이지 이동 함수
  const navigate = useNavigate();
    // ESC 키로 회원가입 창 닫기
    useEffect(() => {

      const handleEsc = (e) => {

        if (e.key === "Escape") {

          closeSignupPage();
        }
      };

      window.addEventListener("keydown", handleEsc);

      return () => {

        window.removeEventListener("keydown", handleEsc);
      };

    }, []);
  

  // 회원가입 창 닫기 함수 , 회원가입 창 닫고 홈 이동
  const closeSignupPage = () => {

    navigate("/");
  };


  // 회원가입 버튼 클릭 함수, 버튼 클릭시 실행
  const handleSignup = async () => {
    
    //비밀번호 재입력 값 비교
    if (password !== confirmPassword) {

        setError("비밀번호가 일치하지 않습니다.");

        return;
      }
    try {

      // 회원가입 API 요청 ,입력값 전달
      // FastAPI / singup 요청 -> 회원가입 처리
      await signup(email, password);

      // 기존 에러 메시지 초기화
      setError("");

      // 회원가입 성공 메시지
      setSuccessMessage("Study GPT 가입을 환영합니다!");


      // 자동 로그인 진행
      const loginResult = await login(email, password);

      // JWT 저장
      saveToken(loginResult.access_token);

      // 이메일 저장
      localStorage.setItem("email", loginResult.email);


      // 홈 이동
      setTimeout(() => {
        window.location.href = "/";
      }, 1200);

    } catch (err) {
      console.log(err);

      // 이메일 중복 가입 에러
      if (
        err.response &&
        err.response.status === 400 //백엔드에서 잘못된 요청 에러 반환 ,회원가입 중복 이메일이 여기 코드에서 걸림.
      ) {
        setError("이미 가입된 이메일입니다.");
      } else {
        setError("회원가입에 실패했습니다.");
      }
    }
  };


  return (
    <div className="relative flex items-center justify-center min-h-screen bg-zinc-950">
      <div className="relative w-full max-w-md p-8 bg-zinc-900 rounded-2xl shadow-lg">
        {/* 회원가입 창 닫기 버튼 */}
        <button
          onClick={closeSignupPage}

          className="
            absolute
            top-4
            right-4

            text-zinc-400
            hover:text-white

            text-2xl
            leading-none

            transition
          "
        >
          ×
        </button>
        <h1 className="text-3xl font-bold text-white text-center mb-6">
          Signup
        </h1>

        {/* 에러 메시지 */}
        {error && (
          <p className="text-red-500 text-sm mb-4">
            {error}
          </p>
        )}

        {/* 회원가입 성공 메시지 */}
        {successMessage && (
          <p className="text-green-400 text-sm mb-4">
            {successMessage}
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
        <div className="mb-4">
          <input
            type="password"
            placeholder="비밀번호 입력"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 rounded-lg bg-zinc-800 text-white outline-none"
          />
        </div>

        {/* 비밀번호 확인 입력 */}
        <div className="mb-6">
          <input
            type="password"
            placeholder="비밀번호 재입력"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}

            className="
              w-full
              p-3
              rounded-lg

              bg-zinc-800
              text-white

              outline-none
            "
          />
        </div>

        {/* 회원가입 버튼 */}
        <button
          type="button"
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