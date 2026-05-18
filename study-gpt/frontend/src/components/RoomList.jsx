//RoomList.jsx

// 왼쪽 채팅방 목록 전용 파일


// React 기본 기능 import
import { useEffect, useState } from "react";

// backend API 요청 객체 import
import api from "../api/api";


// RoomList 컴포넌트
export default function RoomList({

  setSelectedRoom,

  setMessages,

  setIsSidebarOpen

}) {

  // 메인 화면 이동 함수
  const goToHome = () => {

    setSelectedRoom(null);

    setMessages([]);

  };


  // 채팅방 목록 저장 state
  const [rooms, setRooms] = useState([]);


  // 화면 시작 시 자동 실행
  useEffect(() => {

    fetchRooms();

  }, []);


  // backend room 목록 요청 함수
  const fetchRooms = async () => {

    const response = await api.get("/rooms");

    setRooms(response.data);

  };


  return (

    <div>

      {/* 상단 헤더 영역 */}
      <div className="mb-4 space-y-3">

        {/* 로고 + sidebar 버튼 */}
        <div className="flex justify-start pl-[20px]">

          {/* Study GPT 로고 */}
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


      {/* room 배열 반복 출력 */}
      {rooms.map((room) => (

        <div

          key={room.id}

          onClick={() => setSelectedRoom(room)}

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

  );
}