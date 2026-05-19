//RoomList.jsx

// 왼쪽 채팅방 목록 전용 파일


// React 기본 기능 import
import { useEffect, useRef, useState } from "react";

// backend API 요청 객체 import
import api from "../api/api";

//토큰 저장/조회 담당파일 import
import { getToken, removeToken } from "../utils/auth";

//설정 창 컴포넌트 불러오기
import SettingsModal from "./SettingsModal";

//페이지 이동 기능 useNavigate 를 이용해 roomlist에서도 login,signup 페이지로 이동할 수 있게 준비
import { useNavigate } from "react-router-dom";


// RoomList 컴포넌트
export default function RoomList({
  setSelectedRoom,
  setMessages,
  setIsSidebarOpen,
  isSidebarOpen,
  roomRefreshTrigger

}) {
  //페이지 이동 버튼을 사용할 수 있게 navigete 함수를 만듬
  const navigate = useNavigate();

  const [showSidebarContent, setShowSidebarContent] = useState(isSidebarOpen);

  //프로필 메뉴 state추가
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);

  //설정 하위 메뉴 열림 여부 저장
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  //설정 창 열림/ 닫힘 상태 저장
  const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);

  //프로필 메뉴 화면 아무군데나 클릭 시 닫힐 수 있게 함
  const profileMenuRef = useRef(null);

  useEffect(() => {
    if (isSidebarOpen) {
      const timer = setTimeout(() => {
        setShowSidebarContent(true);
      }, 140);

      return () => clearTimeout(timer);
    }
    setShowSidebarContent(false);
  }, [isSidebarOpen]);

  useEffect(() => {

  // ESC 키 처리
  const handleEsc = (e) => {
    if (e.key === "Escape") {
      setIsProfileMenuOpen(false);
    }
  };


  // 바깥 클릭 처리
  const handleClickOutside = (e) => {
    if (
      profileMenuRef.current &&
      !profileMenuRef.current.contains(e.target)
    ) {
      setIsProfileMenuOpen(false);
    }
  };

  window.addEventListener("keydown", handleEsc);
  window.addEventListener("mousedown", handleClickOutside);

  return () => {
    window.removeEventListener("keydown", handleEsc);
    window.removeEventListener("mousedown", handleClickOutside);
  };
}, []);


  // 메인 화면 이동 함수
  const goToHome = () => {
    setSelectedRoom(null);
    setMessages([]);
  };

    // 현재 로그인 토큰 조회,가져오기
  const token = getToken();

  // 현재 로그인 이메일 조회,가져오기
  const email = localStorage.getItem("email");

  // 실제 로그인 여부 판단 (토큰,이메일 전부 존재해야 로그인)
  const isLoggedIn = token && email;

  // 로그아웃 함수
  const handleLogout = () => {

    // JWT 삭제
    removeToken();

    // 이메일 삭제
    localStorage.removeItem("email");

    // React 상태 강제 갱신
    window.location.reload();

  };

  // 채팅방 목록 저장 state
  const [rooms, setRooms] = useState([]);

  // 화면 시작 시 자동 실행
  useEffect(() => {
    const token = getToken();
    //토큰 없으면 rooms 요청 안함
    if (!token) return;
    fetchRooms();
  }, [roomRefreshTrigger]);

  // backend room 목록 요청 함수
  const fetchRooms = async () => {
    const response = await api.get("/rooms");
    setRooms(response.data);
  };
  return (

    // =========================
    // 전체 사이드바 영역
    // =========================
    <div className="flex flex-col h-full">


      {/* =========================
          상단 헤더 영역
      ========================= */}

      {showSidebarContent && (

        <div className="mb-4 space-y-3">

          {/* 로고 영역 */}
          <div className="flex justify-start pl-[20px]">

            <h1
              onClick={goToHome}
              className="
                text-4xl
                font-extrabold
                cursor-pointer
                text-black
                dark:text-white
              "
            >
              Study GPT
            </h1>

          </div>


          {/* 새 채팅 버튼 */}
          <button
            onClick={goToHome}
            className="
              w-full
              bg-blue-500
              text-white
              p-3
              rounded
            "
          >
            + 새 채팅
          </button>

        </div>

      )}


      {/* =========================
          채팅방 목록 영역
      ========================= */}

      {showSidebarContent ? (

        <div className="flex-1 overflow-y-auto">

          {rooms.map((room) => (

            <div
              key={room.id}

              onClick={() => {

                setSelectedRoom(room);

                // 이전 메시지 초기화
                setMessages([]);

              }}

              className="
                p-3 border-b
                border-gray-300
                dark:border-zinc-800

                cursor-pointer

                hover:bg-gray-200
                dark:hover:bg-zinc-800

                text-black
                dark:text-white
              "
            >

              {room.title}

            </div>

          ))}

        </div>

      ) : (

        // 사이드바 닫혔을 때 공간 유지
        <div className="flex-1" />

      )}


      {/* 하단 계정 영역 */}
      <div
        className="
          border-t border-gray-300 dark:border-zinc-800
          mt-2
          p-4
        "
      >
        {/* 로그인 상태 */}
        {isLoggedIn ? (
          <div
            onClick={() => setIsProfileMenuOpen((prev) => !prev)}
            className="
              relative
              h-12
              w-full
              pl-2
              cursor-pointer
              group
            "
          >
            {/* 프로필 hover 배경 */}
            <div
              className={`
                absolute
                bg-transparent
                group-hover:bg-zinc-800
                transition

                ${isSidebarOpen
                  ? "left-[-15px] right-0 top-0 bottom-0 rounded-xl"
                  //사이드바 닫혔을때 hover 이펙트 크기 조절
                  : "left-[-21px] top-1/2 -translate-y-1/2 w-[57px] h-[57px] rounded-full"}
              `}
            />

            {/* 원형 프로필 */}
          <div
            className="
              absolute
              z-10
              left-[-15px]
              top-1/2
              -translate-y-1/2

              w-10 h-10
              rounded-full
              bg-blue-500

              flex items-center justify-center

              text-white
              font-bold
            "
          >
            {email?.charAt(0)?.toUpperCase()}
          </div>

          {/* 펼쳐졌을 때 계정 정보 */}
          <div
            className={`
              absolute
              z-10
              left-14
              top-1/2
              -translate-y-1/2

              flex flex-col

              transition-opacity duration-150

              ${isSidebarOpen && showSidebarContent
                ? "opacity-100"
                : "opacity-0 pointer-events-none"}
            `}
          >
            <div className="text-white text-sm font-semibold whitespace-nowrap">
              {email}
            </div>

            <div className="text-zinc-400 text-xs whitespace-nowrap">
              구독중
            </div>
          </div>
          {/* 프로필 메뉴 */}
          {isProfileMenuOpen && (
            <div
              ref={profileMenuRef}
              className="
                absolute
                bottom-14
                left-0

                w-52

                bg-zinc-900
                border border-zinc-700

                rounded-2xl
                shadow-xl

                p-2

                z-50
              "
            >
              {/* 설정 */}
              <button
                onClick={() => {
                  setIsProfileMenuOpen(false); //프로필 dropdown 닫기
                  setIsSettingsModalOpen(true); //설정창 열기
                }} 
                className="
                  w-full
                  text-left

                  px-4 py-3
                  rounded-xl

                  hover:bg-zinc-800
                  transition

                  text-white
                "
              >
                설정
              </button>

              {/* 로그아웃 */}
              <button
                onClick={handleLogout}
                className="
                  w-full
                  text-left

                  px-4 py-3
                  rounded-xl

                  hover:bg-zinc-800
                  transition

                  text-red-400
                "
              >
                로그아웃
              </button>

              
            </div>
          )}
          </div>
        ) : (
          <div className="relative h-20 w-full -mt-2">
            {/* 접힌 상태 아이콘 */}
            <div
              className={`
                absolute
                left-1/2
                top-1/2
                -translate-x-1/2
                -translate-y-1/2

                transition-opacity duration-150

                ${isSidebarOpen
                  ? "opacity-0 pointer-events-none"
                  : "opacity-100"}
              `}
            >
              <div
                onClick={() => navigate("/login")}
                className="
                  w-10 h-10
                  rounded-full
                  bg-zinc-600
                  flex items-center justify-center
                  cursor-pointer
                  hover:bg-zinc-500
                  transition
                "
              >
                {/* 파란색 사람 실루엣 아이콘 (text-blue-400으로 색상 제어) */}
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="currentColor" 
                  className="w-5 h-5 text-blue-400"
                >
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
            </div>

            {/* 펼친 상태 로그인/회원가입 버튼 */}
            <div
              className={`
                absolute
                left-0
                top-0

                w-full

                flex flex-col gap-2

                transition-opacity duration-150

                ${isSidebarOpen && showSidebarContent
                  ? "opacity-100"
                  : "opacity-0 pointer-events-none"}
              `}
            >
              <button
                onClick={() => navigate("/login")}
                className="
                  w-full
                  bg-zinc-800
                  hover:bg-zinc-700

                  text-white

                  p-2
                  rounded-lg

                  transition
                "
              >
                로그인
              </button>

              <button
                onClick={() => navigate("/signup")}
                className="
                  w-full
                  bg-white
                  hover:bg-gray-200

                  text-black

                  p-2
                  rounded-lg

                  transition
                "
              >
                회원가입
              </button>
            </div>
          </div>
        )}
      </div>

    {/* 설정창 */}
    {isSettingsModalOpen && (
      <SettingsModal
        onClose={() => setIsSettingsModalOpen(false)}
      />
    )}
    </div>
  );
}