//ChatPage.jsx
// RoomList, ChatMessages, ChatInput 전부 조립하는 부모 페이지

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

  // 현재 room의 메시지 저장 state
  const [messages, setMessages] = useState([]);

  // AI 응답 로딩 상태
  const [isLoading, setIsLoading] = useState(false);

  // 왼쪽 사이드바 열림 여부 state
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  //오른쪽 사이드바 열림 여부 state
  const [isSideChatOpen, setIsSideChatOpen] = useState(true);

  return (
    <>
      {/* 왼쪽 sidebar toggle 버튼 */}
      <button
        onClick={() => setIsSidebarOpen((prev) => !prev)}
        className={`
          fixed top-[19px] z-[100]
          text-3xl
          text-black dark:text-white
          transition-all duration-300
          ${isSidebarOpen ? "left-[250px]" : "left-6"}
        `}
      >
        ☰
      </button>
      {/* 오른쪽 sidechat toggle 버튼 */}
      <button
        onClick={() => setIsSideChatOpen((prev) => !prev)}
        className={`
          fixed top-[12px] z-[100]
          text-3xl
          text-black dark:text-white
          transition-all duration-300
          ${isSideChatOpen ? "right-[270px]" : "right-6"}
        `}
      >
        ✦
      </button>
      <div className="
        flex h-screen
        bg-white text-black
        dark:bg-zinc-950 dark:text-white
      ">
        {/*=====================================*/}
        {/* 왼쪽 sidebar */}
        {/*=====================================*/}
        {isSidebarOpen && (
          <div className="
            w-72 h-screen
            border-r-4 border-gray-300
            dark:border-zinc-800
            bg-white
            dark:bg-zinc-950
            p-4 shrink-0
          ">
            <RoomList
              setSelectedRoom={setSelectedRoom}
              setMessages={setMessages}
              setIsSidebarOpen={setIsSidebarOpen}
            />
          </div>
        )}
        {/*=====================================*/}
        {/* 오른쪽 메인 영역 */}
        {/*=====================================*/}
        <div className="
          flex-1 min-h-screen
          bg-white
          dark:bg-zinc-950
        ">
          {/*=====================================*/}
          {/* 홈 화면 */}
          {/*=====================================*/}
          {!selectedRoom ? (
            <div className="
              h-screen
              flex flex-col
              items-center
              justify-center
            ">
              {/* 메인 로고 */}
              <h1 className="
                text-8xl
                font-bold
                text-blue-400
                mb-10
                -mt-20
              ">
                Study GPT
              </h1>
              {/* 입력창 */}
              <div className="w-[700px]">
                <ChatInput
                  selectedRoom={selectedRoom}
                  setSelectedRoom={setSelectedRoom}
                  setRefreshTrigger={setRefreshTrigger}
                  messages={messages}
                  setMessages={setMessages}
                  isLoading={isLoading}
                  setIsLoading={setIsLoading}
                />
              </div>
            </div>
          ) : (
            /*=====================================*/
            /* 실제 학습 화면 */
            /*=====================================*/
            <div className="
              flex h-screen
              bg-white
              dark:bg-zinc-950
            ">
              {/* 중앙 메인 채팅 */}
              <div className="flex-1 min-w-0 px-6">
                {/* 실제 채팅 영역 */}
                <div className="
                  w-full
                  max-w-5xl
                  mx-auto
                  h-screen
                  flex flex-col
                  p-6
                ">
                  {/* 메시지 영역 */}
                  <div className="flex-1 overflow-y-auto">
                    <ChatMessages
                      selectedRoom={selectedRoom}
                      refreshTrigger={refreshTrigger}
                      messages={messages}
                      setMessages={setMessages}
                      isLoading={isLoading}
                    />
                  </div>
                  {/* 입력창 */}
                  <ChatInput
                    selectedRoom={selectedRoom}
                    setSelectedRoom={setSelectedRoom}
                    setRefreshTrigger={setRefreshTrigger}
                    messages={messages}
                    setMessages={setMessages}
                    isLoading={isLoading}
                    setIsLoading={setIsLoading}
                  />
                </div>
              </div>
              {/* 오른쪽 Side Chat */}
              {isSideChatOpen && (
                <div className="
                  w-72 h-screen shrink-0
                  border-l-4 border-gray-300
                  dark:border-zinc-800
                  bg-white
                  dark:bg-zinc-950
                  p-4
                ">
                  <h2 className="
                    text-xl
                    font-bold
                    text-black
                    dark:text-white
                    mb-4
                    pl-[88px]
                  ">
                    Side Chat
                  </h2>
                  <div className="
                    text-gray-600
                    dark:text-gray-500
                  ">
                    학습 중 궁금한 내용을 빠르게
                    <br />
                    질문할 수 있습니다.
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </>
  );   
}