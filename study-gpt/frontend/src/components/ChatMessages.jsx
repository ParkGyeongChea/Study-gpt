//ChatMessages.jsx

// 현재 선택한 room의 이전 대화 출력 컴포넌트


// React 기본 기능 import
import { useEffect } from "react";

// backend API 요청 객체 import
import api from "../api/api";


// ChatMessages 컴포넌트
export default function ChatMessages({

  selectedRoom,

  refreshTrigger,

  messages,

  setMessages,

  isLoading

}) {

  // selectedRoom 또는 refreshTrigger 변경 시 실행
  useEffect(() => {

    // room 선택 안 된 상태면 중지
    if (!selectedRoom) return;


    // 현재 room 메시지 조회
    fetchMessages();

  }, [selectedRoom, refreshTrigger]);


  // backend 메시지 조회 함수
  const fetchMessages = async () => {

    const response = await api.get(

      `/rooms/${selectedRoom.id}/messages`

    );

    // 메시지 저장
    setMessages(response.data);

  };


  return (

    <div className="space-y-3">

      {/* messages 배열 반복 출력 */}
      {messages.map((message) => (

        <div

          key={message.id}

          className="
            p-4 rounded-xl border

            border-gray-300
            dark:border-zinc-800

            bg-white
            dark:bg-zinc-900

            text-black
            dark:text-white
          "

        >

          {/* 메시지 작성자(role) */}
          <div className="font-bold text-blue-400 mb-2">

            {message.role}

          </div>


          {/* 실제 메시지 내용 */}
          <div>

            {message.content}

          </div>

        </div>

      ))}


      {/* AI 응답 생성 중 표시 */}
      {isLoading && (

        <div className="
          p-4 rounded-xl border

          border-gray-300
          dark:border-zinc-800

          bg-white
          dark:bg-zinc-900

          text-gray-700
          dark:text-gray-300
        ">

          생각 중...

        </div>

      )}

    </div>

  );
}