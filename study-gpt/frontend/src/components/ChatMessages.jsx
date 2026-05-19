//ChatMessages.jsx

// 현재 선택한 room의 이전 대화 출력 컴포넌트


// React 기본 기능 import
//useRef = 특정 HTML 위치 기억하는 리액트 기능
import { useEffect, useRef } from "react";

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

  // 맨 아래 위치 추적 ref
  const bottomRef = useRef(null);

  // selectedRoom 또는 refreshTrigger 변경 시 실행
  useEffect(() => {

    // room 없으면 중지
  if (!selectedRoom) return;

  // 현재 messages 이미 있으면 fetch 안 함
  if (messages.length > 0) return;

  fetchMessages();

}, [selectedRoom, refreshTrigger]);

  // 새 메시지 생성 시 자동 스크롤
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      //scrollIntoView = 해당 위치까지 이동
      behavior: "smooth" //부드럽게 스크롤
    });
  }, [messages]); // 메시지 변경될 때마다, 메시지 위치인 맨 아래로 부드럽게 스크롤


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

          className={`
            
            w-full

            ${
              message.role === "user"

                ? "flex justify-end"

                : "flex justify-start"
            }

          `}
        >

          {/* 사용자 메시지 */}
          {message.role === "user" ? (

            <div
              className="
                max-w-[85%]

                px-5
                py-3

                rounded-full

                bg-zinc-900
                text-white

                whitespace-pre-wrap
              "
            >

              {message.content}

            </div>

          ) : (

            /* AI 메시지 */
            <div
              className="
                w-full

                text-black
                dark:text-white

                whitespace-pre-wrap

                leading-8
              "
            >

              {message.content}

            </div>

          )}

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
      
      {/* 자동 스크롤용 맨 아래 위치 */}
      <div ref={bottomRef}></div>

    </div>

  );
}