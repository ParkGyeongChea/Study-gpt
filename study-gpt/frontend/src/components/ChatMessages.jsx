//ChatMessages.jsx

//현재 선택한 room의 이전 대화 출력 전용 컴포넌트
//이전 대화 출력, user / assistant 구분 , 채팅 말풍선, 스크롤 ,실시간 추가 여기서 담당

// React 기본 기능 import
import { useEffect, useState } from "react";

// backend API 요청 객체 import
import api from "../api/api";


// ChatMessages 컴포넌트
// selectedRoom + refreshTrigger 전달받음
export default function ChatMessages({
  selectedRoom,
  refreshTrigger
}) {


  // 현재 room 메시지 저장 state
  const [messages, setMessages] = useState([]);
  // messages = 현재 room 메시지 목록
  // setMessages = 메시지 목록 변경 함수


  // selectedRoom 또는 refreshTrigger 변경 시 실행
  useEffect(() => {

    // room 선택 안 된 상태면 실행 중지
    if (!selectedRoom) return;


    // 현재 room 메시지 조회 함수 실행
    fetchMessages();

  }, [selectedRoom, refreshTrigger]);
  // selectedRoom 변경 시 실행
  // refreshTrigger 변경 시도 실행
  // 즉 메시지 전송 후 자동 재조회 가능


  // backend 메시지 조회 함수
  const fetchMessages = async () => {

    // GET /rooms/{room_id}/messages 요청
    const response = await api.get(
      `/rooms/${selectedRoom.id}/messages`
    );
    // 현재 room 메시지 조회


    // 응답 메시지 저장
    setMessages(response.data);
    // state 변경 시 화면 자동 업데이트
  };


  return (

    <div className="space-y-3">
      {/* space-y-3 = 메시지끼리 세로 간격 */}


      {/* messages 배열 반복 출력 */}
      {messages.map((message) => (

        <div
          key={message.id}
          className="p-3 border rounded"
        >
          {/* p-3 = 안쪽 여백 */}
          {/* border = 테두리 */}
          {/* rounded = 모서리 둥글게 */}


          {/* 메시지 작성자(role) 출력 */}
          <div className="font-bold">
            {/* font-bold = 글자 굵게 */}

            {message.role}

          </div>


          {/* 실제 메시지 내용 출력 */}
          <div>
            {message.content}
          </div>

        </div>

      ))}

    </div>
  );
}