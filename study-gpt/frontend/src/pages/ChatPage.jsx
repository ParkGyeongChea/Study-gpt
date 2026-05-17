//ChatPage.jsx
// RoomList,ChatMessages,ChatInput 전부 조립하는 부모 페이지

//====================================
// React 상태(state) 기능 import
import { useState } from "react";

// 채팅방 목록 컴포넌트 import
import RoomList from "../components/RoomList";

// 이전 대화 출력 컴포넌트 import
import ChatMessages from "../components/ChatMessages";

// 메시지 입력 컴포넌트 import
import ChatInput from "../components/ChatInput";


export default function ChatPage() {

  // 현재 선택된 room 저장 state
  const [selectedRoom, setSelectedRoom] = useState(null);

  // 메시지 새로고침용 state
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  // 숫자 변경 시 ChatMessages 재조회용
  // 처음엔 0


  return (

    <div className="flex h-screen">
      {/* flex = 가로 배치 */}
      {/* h-screen = 화면 전체 높이 */}


      {/* 왼쪽 room 목록 영역 */}
      <div className="w-80 border-r border-gray-300 p-4">
        {/* w-80 = 가로 너비 고정 */}
        {/* border-r = 오른쪽 테두리 */}
        {/* border-gray-300 = 연한 회색 선 */}
        {/* p-4 = 안쪽 여백 */}

        <RoomList
          setSelectedRoom={setSelectedRoom}
        />

      </div>


      {/* 오른쪽 채팅 영역 */}
      <div className="flex-1 p-4 flex flex-col">
        {/* flex-1 = 남은 공간 전부 사용 */}
        {/* p-4 = 안쪽 여백 */}
        {/* flex = 내부 요소 flex 사용 */}
        {/* flex-col = 세로 배치 */}


        {selectedRoom ? (

          <>
            {/* 이전 대화 출력 */}
            <ChatMessages
              selectedRoom={selectedRoom}
              refreshTrigger={refreshTrigger}
            />
            {/* refreshTrigger 전달 */}
            {/* 값 변경 시 메시지 재조회 가능 */}


            {/* 메시지 입력창 */}
            <ChatInput
              selectedRoom={selectedRoom}
              setRefreshTrigger={setRefreshTrigger}
            />
            {/* setRefreshTrigger 전달 */}
            {/* 메시지 전송 후 refreshTrigger 변경 가능 */}

          </>

        ) : (

          <div>채팅방을 선택하세요</div>

        )}

      </div>

    </div>
  );
}