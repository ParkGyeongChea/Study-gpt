//ChatPage.jsx
// RoomList, ChatMessages, ChatInput 전부 조립하는 부모 페이지

//====================================
import { useState, useEffect } from "react";
import RoomList from "../components/RoomList";
import ChatMessages from "../components/ChatMessages";
import ChatInput from "../components/ChatInput";
import { useNavigate } from "react-router-dom";


export default function ChatPage() {

  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [studyMode, setStudyMode] = useState("free");
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [messages, setMessages] = useState([]);
  const [sideMessages, setSideMessages] = useState(() => {

    
    const savedMessages = localStorage.getItem("sideMessages");

    return savedMessages
      ? JSON.parse(savedMessages)
      : [];

  });

  
  const [sideInput, setSideInput] = useState("");
  const [isSideLoading, setIsSideLoading] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [roomRefreshTrigger, setRoomRefreshTrigger] = useState(0);
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isSideChatOpen, setIsSideChatOpen] = useState(false);
  const [showSideChatContent, setShowSideChatContent] = useState(true);
  const handleSetSelectedRoom = (room) => {
    
    setIsSideChatOpen(false);

    
    setSelectedRoom(room);

  };

  
  useEffect(() => {

    if (isSideChatOpen) {

      const timer = setTimeout(() => {
        setShowSideChatContent(true);
      }, 200);

      return () => clearTimeout(timer);
    }

    setShowSideChatContent(false);

  }, [isSideChatOpen]);

  
  useEffect(() => {

    localStorage.setItem(
      "sideMessages",
      JSON.stringify(sideMessages)
    );

  }, [sideMessages]);

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black">

      {/* 왼쪽 sidebar toggle 버튼 */}
      <button
        onClick={() => setIsSidebarOpen((prev) => !prev)}
        className={`
          fixed top-[19px] z-[100]
          text-3xl
          text-black dark:text-white
          transition-[left] duration-300
          ${isSidebarOpen ? "left-[250px]" : "left-6"}
        `}
      >
        ☰
      </button>

      {/* 오른쪽 sidechat toggle 버튼 */}
        {selectedRoom && (
        <button
          onClick={() => setIsSideChatOpen((prev) => !prev)}
          className={`
            fixed top-[12px] z-[100]
            text-3xl
            text-black dark:text-white
            transition-[right] duration-300
            ${isSideChatOpen ? "right-[270px]" : "right-6"}
          `}
        >
          ✦
        </button>
      )}

      <div
        className="
          flex h-screen
          bg-white text-black
          dark:bg-zinc-950 dark:text-white
        "
      >
        {/* 왼쪽 sidebar */}
        <div
          className={`
            h-screen
            border-r-4 border-gray-300
            dark:border-zinc-800
            bg-white
            dark:bg-zinc-950
            p-4 shrink-0
            transition-[width] duration-300

            ${isSidebarOpen ? "w-72" : "w-20"}
          `}
        >
          <RoomList
            selectedRoom={selectedRoom}
            setSelectedRoom={handleSetSelectedRoom}
            setMessages={setMessages}
            setIsSidebarOpen={setIsSidebarOpen}
            isSidebarOpen={isSidebarOpen}
            roomRefreshTrigger={roomRefreshTrigger}
          />
        </div>

        {/* 오른쪽 메인 영역 */}
        <div
          className="
            flex-1 min-h-screen
            bg-white
            dark:bg-zinc-950
          "
        >
          {!selectedRoom && messages.length === 0 ? (
            <div
              className="
                h-screen
                flex flex-col
                items-center
                justify-center
              "
            >
              <h1
                className="
                  text-8xl
                  font-bold
                  text-blue-400
                  mb-10
                  -mt-20
                "
              >
                Study GPT
              </h1>

              <div className="w-[700px]">
                <ChatInput
                  selectedRoom={selectedRoom}
                  setSelectedRoom={handleSetSelectedRoom}
                  setRoomRefreshTrigger={setRoomRefreshTrigger}
                  setRefreshTrigger={setRefreshTrigger}
                  messages={messages}
                  setMessages={setMessages}
                  isLoading={isLoading}
                  setIsLoading={setIsLoading}
                  studyMode={studyMode}
                  setStudyMode={setStudyMode}
                />
              </div>
            </div>
          ) : (
            <div
              className="
                flex h-screen
                bg-white
                dark:bg-zinc-950
              "
            >
              <div className="
                    flex-1
                    min-w-0
                    px-6

                    transition-all
                    duration-300
                  ">
                <div
                  className="
                    w-[1100px]
                    max-w-full
                    mx-auto
                    h-screen
                    flex flex-col
                    p-6
                  "
                >
                  <div className="flex-1 overflow-y-auto">
                    <ChatMessages
                      selectedRoom={selectedRoom}
                      refreshTrigger={refreshTrigger}
                      messages={messages}
                      setMessages={setMessages}
                      isLoading={isLoading}
                    />
                  </div>
                  
                    <ChatInput
                      selectedRoom={selectedRoom}
                      setSelectedRoom={handleSetSelectedRoom}
                      setRoomRefreshTrigger={setRoomRefreshTrigger}
                      setRefreshTrigger={setRefreshTrigger}
                      messages={messages}
                      setMessages={setMessages}
                      isLoading={isLoading}
                      setIsLoading={setIsLoading}
                      studyMode={studyMode}
                      setStudyMode={setStudyMode}
                    />
                </div>
              </div>

              <div
                className={`
                  relative h-screen
                  shrink-0
                  overflow-hidden

                  bg-white
                  dark:bg-zinc-950

                  transition-[width] duration-300

                  ${selectedRoom
                    ? (
                        isSideChatOpen
                          ? "w-72 border-l-4 border-gray-300 dark:border-zinc-800"
                          : "w-0 border-l-0"
                      )
                    : "w-0 p-0 border-l-0"
                  }
                `}
              >

                <div
                  className={`
                    h-full
                    p-4

                    flex
                    flex-col

                    transition-opacity duration-150

                    ${showSideChatContent
                      ? "opacity-100"
                      : "opacity-0"}
                  `}
                >

                  <div
                    className="
                      flex
                      items-center
                      justify-between
                      mb-4
                    "
                  >

                    <h2
                      className="
                        flex-1
                        text-center
                        pl-[25px]
                        text-xl
                        font-bold
                        text-black
                        dark:text-white
                      "
                    >
                      Side Chat
                    </h2>

                    <button
                      onClick={() => {

                        // 사이드챗 메시지 초기화
                        setSideMessages([]);

                        // localStorage 데이터 제거
                        localStorage.removeItem("sideMessages");

                      }}

                      className="
                        text-sm
                        font-semibold
                        text-gray-400
                        hover:text-white
                        transition
                        -translate-x-[8px]
                      "
                    >
                      Clear
                    </button>

                  </div>

                  <div
                    className="
                      text-gray-600
                      dark:text-gray-500
                    "
                  >
                    학습 중 궁금한 내용을 빠르게
                    <br />
                    질문할 수 있습니다.
                  </div>
                  {/* 사이드챗 메시지 출력 영역 */}
                  <div
                    className="
                      mt-6
                      flex-1
                      overflow-y-auto

                      flex
                      flex-col
                      gap-3

                      pr-1
                    "
                  >
                    {/* sideMessages 안에 들어있는 메시지들을 하나씩 화면에 출력 */}
                    {sideMessages.map((msg, index) => (
                      <div
                        key={index}
                        className={`
                          p-3
                          rounded-2xl
                          text-sm
                          whitespace-pre-wrap
                          ${
                            //이 메시지가 사용자 메시지인지 검사하는 코드
                            msg.role === "user"
                              ? `
                                bg-blue-500
                                text-white
                                self-end
                              `
                              : `
                                bg-zinc-800
                                text-white
                                self-start
                              `
                          }
                        `}
                      >
                        {msg.content}
                      </div>
                    ))}

                  </div>
                  {/* 사이드챗 입력 영역 */}
                  <div
                    className="
                    mt-auto
                    pt-4
                    pb-2
                    w-full
                    flex
                    items-center
                    gap-2"
                  >
                    <input
                      type="text"
                      value={sideInput}
                      //사용자가 입력할 때마다 sideInput state 업데이트
                      onChange={(e) => {
                        setSideInput(e.target.value);
                      }}
                      onKeyDown={(e) => {

                      // Enter 입력 시 전송 버튼 클릭
                      if (e.key === "Enter") {
                        e.preventDefault();
                        document.getElementById("side-chat-send-btn")?.click();
                      }
                    }}

                      placeholder="질문해보세요..."

                      className="
                        flex-1
                        min-w-0
                        rounded-xl
                        bg-zinc-900
                        border border-zinc-700
                        px-4
                        py-3
                        text-white
                        outline-none
                      "
                    />

                    <button

                      id="side-chat-send-btn"
                      onClick={async () => {

                        // 빈 입력 방지
                        if (!sideInput.trim()) return;
                        // 사용자 메시지 저장
                        const userMessage = {
                          role: "user",
                          content: sideInput
                        };

                        // 화면에 사용자 메시지 먼저 추가
                        setSideMessages((prev) => [
                          ...prev,
                          userMessage
                        ]);

                        // 입력창 비우기
                        setSideInput("");

                        // 로딩 시작
                        setIsSideLoading(true);

                        try {
                          // 백엔드 side-chat API 요청
                          const response = await fetch(
                            "https://study-gpt-backend.onrender.com",
                            {
                              method: "POST",

                              headers: {
                                "Content-Type": "application/json"
                              },

                              body: JSON.stringify({
                                message: userMessage.content
                              })
                            }
                          );
                          // JSON 응답 변환
                          const data = await response.json();

                          // AI 메시지 저장
                          const aiMessage = {
                            role: "assistant",
                            content: data.message
                          };

                          // 화면에 AI 응답 추가
                          setSideMessages((prev) => [
                            ...prev,
                            aiMessage
                          ]);

                        } catch (error) {
                          console.error("사이드챗 오류:", error);
                        } finally {

                          // 로딩 종료
                          setIsSideLoading(false);
                        }

                      }}
                      className="
                        h-[52px]
                        w-[56px]
                        shrink-0
                        rounded-xl
                        bg-blue-500
                        text-white
                        hover:bg-blue-600
                        transition
                      "
                    >
                      전송
                    </button>

                  </div>

                </div>

              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );   
}