//ChatInput.jsx
//입력창 + 전송 버튼 담당

// React 상태(state) 기능 import
import { useState } from "react";

// backend API 요청 객체 import
import api from "../api/api";


// ChatInput 컴포넌트
// 부모(ChatPage)에게 selectedRoom 전달받음
// setRefreshTrigger도 전달받음
export default function ChatInput({
  selectedRoom,
  setRefreshTrigger
}) {


  // 입력창 값 저장 state
  const [message, setMessage] = useState("");
  // message = 현재 입력값 저장
  // setMessage = 입력값 변경 함수


  // 전송 버튼 클릭 함수
  const handleSend = async () => {

    // 빈 문자열이면 전송 중지
    if (!message.trim()) return;
    // trim() = 앞뒤 공백 제거
    // 공백만 입력한 경우 방지


    // POST /agent 요청
    await api.post("/agent", {

      room_id: selectedRoom.id,
      // 현재 선택된 room id 전달

      message: message,
      // 사용자 입력 메시지 전달

      study_mode: "free"
      // 현재는 free 모드 고정

    });


    // refreshTrigger 변경
    setRefreshTrigger((prev) => prev + 1);
    // prev = 이전 값
    // 이전 값 +1 해서 refreshTrigger 변경
    // 숫자 바뀌면 ChatMessages 재조회 가능


    // 입력창 초기화
    setMessage("");
  };


  return (

    <div className="flex gap-2 mt-4">
      {/* flex = 가로 배치 */}
      {/* gap-2 = 요소 사이 간격 */}
      {/* mt-4 = 위쪽 바깥 여백 */}


      {/* 메시지 입력창 */}
      <input

        type="text"

        value={message}
        // 입력값 state 연결

        onChange={(e) => setMessage(e.target.value)}
        // 입력 시 message state 변경

        placeholder="메시지를 입력하세요"

        className="flex-1 border rounded p-3"
        // flex-1 = 남은 공간 전부 사용
        // border = 테두리
        // rounded = 모서리 둥글게
        // p-3 = 안쪽 여백
      />


      {/* 전송 버튼 */}
      <button

        onClick={handleSend}
        // 클릭 시 handleSend 실행

        className="bg-blue-500 text-white px-4 rounded"
      >
        {/* bg-blue-500 = 파란 배경 */}
        {/* text-white = 흰 글자 */}
        {/* px-4 = 좌우 안쪽 여백 */}
        {/* rounded = 모서리 둥글게 */}

        전송

      </button>

    </div>
  );
}