//ChatInput.jsx
// 입력창 + 메시지 전송 담당 컴포넌트

//=====================================

// React 상태(state) 기능 import
import { useState } from "react";

// backend API 요청 객체 import
import api from "../api/api";


// ChatInput 컴포넌트
export default function ChatInput({

  selectedRoom,
  // 현재 선택된 채팅방 객체

  setSelectedRoom,
  // 현재 선택 room 변경 함수

  setRoomRefreshTrigger,
  //현재 선택 room 초기화 함수

  setRefreshTrigger,
  // ChatMessages 다시 조회시키는 상태 변경 함수

  messages,
  // 현재 채팅 메시지 배열 state

  setMessages,
  // messages state 변경 함수

  isLoading,
  // 현재 AI 응답 생성 중인지 여부

  setIsLoading
  // AI 로딩 상태 변경 함수

}) {

  // 입력창 값 저장 state
  const [message, setMessage] = useState("");

  // 현재 선택된 학습 모드 저장 state
  const [selectedMode, setSelectedMode] = useState("free");


  //=====================================
  // 메시지 전송 함수
  //=====================================

  const handleSend = async () => {

    // 공백 입력 방지
    if (!message.trim()) return;


    //=====================================
    // user 메시지 즉시 화면 출력
    //=====================================

    const tempMessage = {

      id: Date.now(),

      role: "user",

      content: message

    };


    // 기존 메시지 배열 뒤에 추가
    setMessages((prev) => [...prev, tempMessage]);


    // 현재 room 임시 저장
    let currentRoom = selectedRoom;


    //=====================================
    // room 없는 경우 새 room 생성
    //=====================================

    if (!currentRoom) {

      const roomResponse = await api.post("/rooms", {

        title: "새 채팅"

      });

      currentRoom = roomResponse.data;

      setSelectedRoom(currentRoom);

      //새 채팅방 생성시 다시 조회
      setRoomRefreshTrigger((prev) => prev + 1);

      // room 생성 직후 messages 유지 강제
      setMessages((prev) => [...prev]);

    }


    //=====================================
    // AI 로딩 시작
    //=====================================

    setIsLoading(true);

    // 임시 AI 로딩 메시지
    const loadingMessage = {
      id: "loading",
      role: "assistant",
      content: "답변 생성 중..."
    };
    // 화면에 즉시 출력

    setMessages((prev) => [...prev,loadingMessage]);

    //=====================================
    // backend AI 요청
    //=====================================

    try {

      const response = await api.post("/agent", {

        room_id: currentRoom.id,

        message: message,

        study_mode: selectedMode

      });

      // agent_service에서 채팅방 제목이 자동 변경되었을 수 있으므로
      // RoomList를 다시 조회시킴
      setRoomRefreshTrigger((prev) => prev + 1);


      // assistant 메시지 생성
      const assistantMessage = {

        id: Date.now() + 1,

        role: "assistant",

        content: response.data.lecture.content

      };


      // assistant 메시지 추가
      setMessages((prev) => [
        
        // loading 메시지 제거
        ...prev.filter((msg) => msg.id !== "loading"),

         // 실제 AI 응답 추가
        assistantMessage
      ]);


      // ChatMessages 재조회 trigger
      setRefreshTrigger((prev) => prev + 1);

    } catch (error) {

      console.log(error.response?.data);

    } finally {

      // AI 로딩 종료
      setIsLoading(false);

    }


    // 입력창 초기화
    setMessage("");

  };


  //=====================================
  // 화면 출력(UI)
  //=====================================

  return (

    <div className="mt-6">

      {/* 전체 입력 박스 */}
      <div className="
        bg-white
        dark:bg-zinc-900

        border-[3px]

        border-gray-300
        dark:border-zinc-700

        rounded-[2rem]
        p-4
      ">

        {/* 실제 메시지 입력창 */}
        <input

          type="text"

          value={message}

          onChange={(e) => setMessage(e.target.value)}

          placeholder="무엇을 배우고 싶나요?"


          // Enter 입력 시 메시지 전송
          onKeyDown={(e) => {

            if (e.key === "Enter") {

              handleSend();

            }

          }}


          className="
            w-full
            bg-transparent
            outline-none

            text-black
            dark:text-white

            text-lg

            placeholder:text-gray-500
            dark:placeholder:text-gray-400
          "

        />


        {/* 아래 옵션 영역 */}
        <div className="flex justify-end mt-4">

          {/* 학습 모드 선택 dropdown */}
          <select

            value={selectedMode}

            onChange={(e) => setSelectedMode(e.target.value)}

            className="
              bg-gray-100
              dark:bg-zinc-800

              text-black
              dark:text-white

              border border-gray-300
              dark:border-zinc-700

              rounded-full
              px-4 py-2
              text-sm
            "

          >

            <option value="free">
              자유 학습
            </option>

            <option value="light_quiz">
              가벼운 확인
            </option>

            <option value="strict_quiz">
              집중 학습
            </option>

          </select>

        </div>

      </div>

    </div>

  );
}