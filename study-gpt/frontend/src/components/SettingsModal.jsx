// SettingsModal.jsx
// 설정 창 담당 컴포넌트

import { useEffect, useState } from "react";

//axios 백엔드 api 요청 라이브러리 가져오기
import axios from "axios";

//JWT 토큰 삭제 함수 가져오기
import { removeToken } from "../utils/auth";

function SettingsModal({ onClose }) {

  // 현재 선택된 설정 탭 상태
  const [activeTab, setActiveTab] = useState("general");

  // 회원탈퇴 경고창 상태
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  //회원탈퇴 함수 추가
  const handleDeleteAccount = async () => {
    try {

    // JWT 토큰 가져오기
    const token = localStorage.getItem("token");

    // 회원탈퇴 API 요청 (DELETE /users/me 요청)
    await axios.delete("http://localhost:8000/users/me",
      {headers: { Authorization: `Bearer ${token}`}}); // Authorization = JWT 로그인 토큰 전달

    // JWT 삭제
    removeToken();

    // 이메일 삭제
    localStorage.removeItem("email");

    // 메인 페이지 이동
    window.location.href = "/";

  } catch (err) {
    console.log(err);
    alert("회원탈퇴 중 오류가 발생했습니다.");
  }
};

  // ESC 누르면 설정창 닫기
  useEffect(() => {

    const handleEsc = (e) => {
      if (e.key === "Escape") {
        onClose();
      }
    };

    window.addEventListener("keydown", handleEsc);

    return () => {
      window.removeEventListener("keydown", handleEsc);
    };

  }, [onClose]);


  return (

    // 전체 배경
    <div
      onClick={onClose}
      className="
        fixed
        inset-0

        bg-black/60

        flex
        items-center
        justify-center

        z-[200]
      "
    >

      {/* 설정창 */}
      {/* relative = absolute 기준점 생성, x버튼이 설정창 기준 우측 상단에 붙음 */}
      <div
        onClick={(e) => e.stopPropagation()}
        className=" 
          relative 
          w-[900px]
          h-[650px]
          bg-zinc-900
          rounded-2xl
          border border-zinc-800
          flex
          overflow-hidden
        "
      >

        {/* 왼쪽 메뉴 */}
        <div
          className="
            w-[260px]

            border-r border-zinc-800

            p-4
          "
        >
            {/* 설정창 닫기 버튼 */}
            <button
            onClick={onClose}
            className="
                absolute
                top-5
                right-5

                text-zinc-400
                hover:text-white

                text-3xl
                leading-none

                transition
            "
            >
            ×
            </button>

          {/* 제목 */}
          <h2 className="text-white text-2xl font-bold mb-6">
            설정
          </h2>

          {/* 일반 탭 */}
          <button
            onClick={() => setActiveTab("general")}
            className={`
              w-full
              text-left

              px-4 py-3
              rounded-xl

              mb-2

              transition

              ${activeTab === "general"
                ? "bg-zinc-800 text-white"
                : "text-zinc-400 hover:bg-zinc-800"}
            `}
          >
            일반
          </button>

          {/* 계정 탭 */}
          <button
            onClick={() => setActiveTab("account")}
            className={`
              w-full
              text-left

              px-4 py-3
              rounded-xl

              transition

              ${activeTab === "account"
                ? "bg-zinc-800 text-white"
                : "text-zinc-400 hover:bg-zinc-800"}
            `}
          >
            계정
          </button>

        </div>


        {/* 오른쪽 내용 */}
        <div className="flex-1 p-8 overflow-y-auto">

          {/* 일반 탭 */}
          {activeTab === "general" && (
            <div>

              <h2 className="text-white text-3xl font-bold mb-8">
                일반
              </h2>

              <p className="text-zinc-400">
                추후 설정 기능이 추가될 예정입니다.
              </p>

            </div>
          )}


          {/* 계정 탭 */}
          {activeTab === "account" && (
            <div>

              <h2 className="text-white text-3xl font-bold mb-8">
                계정
              </h2>

              {/* 이메일 */}
              <div className="mb-8">

                <p className="text-zinc-500 text-sm mb-2">
                  이메일
                </p>

                <p className="text-white text-lg">
                  {localStorage.getItem("email")}
                </p>

              </div>


              {/* 회원탈퇴 버튼 */}
              <button
                onClick={() => setShowDeleteConfirm(true)}
                className="
                  px-5 py-3

                  rounded-xl

                  bg-red-600
                  hover:bg-red-700

                  text-white
                  font-semibold

                  transition
                "
              >
                회원 탈퇴
              </button>

            </div>
          )}

        </div>

      </div>


      {/* 회원탈퇴 경고 모달 */}
      {showDeleteConfirm && (
        <div
          className="
            fixed
            inset-0

            bg-black/70

            flex
            items-center
            justify-center

            z-[300]
          "
        >

          <div
            className="
              w-[420px]

              bg-zinc-900

              rounded-2xl

              border border-zinc-800

              p-6
            "
          >

            <h3 className="text-white text-2xl font-bold mb-4">
              정말 탈퇴하시겠습니까?
            </h3>

            <p className="text-zinc-400 mb-8 leading-relaxed">
              삭제된 학습 데이터와 채팅은 복구할 수 없습니다.
            </p>


            {/* 버튼 영역 */}
            <div className="flex justify-end gap-3">

              {/* 취소 */}
              <button
                onClick={() => setShowDeleteConfirm(false)}
                className="
                  px-4 py-2

                  rounded-lg

                  bg-zinc-800
                  hover:bg-zinc-700

                  text-white

                  transition
                "
              >
                취소
              </button>


              {/* 최종 회원탈퇴 */}
              <button
                onClick={handleDeleteAccount}
                className="
                  px-4 py-2

                  rounded-lg

                  bg-red-600
                  hover:bg-red-700

                  text-white

                  transition
                "
              >
                회원 탈퇴
              </button>

            </div>

          </div>

        </div>
      )}

    </div>
  );
}

export default SettingsModal;