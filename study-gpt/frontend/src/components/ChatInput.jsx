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

  setIsLoading,
  // AI 로딩 상태 변경 함수

  studyMode,
  setStudyMode
  //학습 모드 저장

}) {

  // 입력창 값 저장 state
  const [message, setMessage] = useState("");

  // 현재 선택된 학습 모드 저장 state
  //const [selectedMode, setSelectedMode] = useState("free");


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

    // 입력창 즉시 초기화
    setMessage("");

    
    
    // 기존 메시지 배열 뒤에 추가
    setMessages((prev) => [...prev, tempMessage]);


    // 현재 room 임시 저장
    let currentRoom = selectedRoom;

    // 현재 로그인 토큰 확인
    const token = localStorage.getItem("token");


    //=====================================
    // room 없는 경우, 로그인 상태일 떄만 생성
    //=====================================

    if (!currentRoom && token) {
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

    // 사용자 메시지 전송 즉시 room 목록 새로고침
    if (currentRoom?.id) {
      setRoomRefreshTrigger((prev) => prev + 1);
    }


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
    // agent 요청 데이터 생성

    const requestData = {

      message: message,

      study_mode: studyMode
    };
    
    // 로그인 상태일 때만 room_id 추가
    if (currentRoom?.id) {

      requestData.room_id = currentRoom.id;
    }

    try {

      

      const response = await api.post("/agent", requestData);

     
      // agent_service에서 채팅방 제목이 자동 변경되었을 수 있으므로
      // RoomList를 다시 조회시킴
      setRoomRefreshTrigger((prev) => prev + 1);


      // assistant 메시지 배열 생성
      const newMessages = [];

      // 강의 + 퀴즈를 하나의 assistant message로 합치기
      let assistantContent = "";

      // 강의 내용 추가
      if (response.data?.lecture?.content) {
        assistantContent += response.data.lecture.content;
      }

      // 퀴즈 내용 추가
      if (response.data?.quiz) {
        const quizBlocks = response.data.quiz.map((quiz, index) => {
          const choicesText = quiz.choices
            .map((choice, choiceIndex) => `(${choiceIndex + 1}) ${choice}`)
            .join("\n\n");

          return [
            "---",
            "",
            `## 📝 학습 확인 퀴즈 ${index + 1}`,
            "",
            quiz.question,
            "",
            choicesText
          ].join("\n");
        });

        const quizText = [
          "---",
          "",
          "# 📝 이번 챕터에서 배운 내용을 간단한 퀴즈로 체크해보세요!",
          "",
          "## 답변 예시",
          "- 1,2",
          "- 1번, 2번",
          "",
          "💡 만약 문제를 다시 풀고 싶으시면 '다시 문제 내줘' 라고 입력해보세요!",
          "",
          quizBlocks.join("\n\n")
        ].join("\n");

        assistantContent += "\n\n" + quizText;
      }

      // 최종 assistant 메시지 추가
      if (assistantContent) {
        newMessages.push({
          id: Date.now() + 1,
          role: "assistant",
          content: assistantContent
        });
      }

      // 일반 message 응답 추가
      if (response.data?.message) {
        newMessages.push({
          id: Date.now() + 3,
          role: "assistant",
          content: response.data.message
        });
      }

      // assistant 메시지 추가
      setMessages((prev) => {

        // loading 메시지만 제거
        const filteredMessages = prev.filter(
          (msg) => msg.id !== "loading"
        );

        // 기존 메시지 유지 + 배열 안 메시지들을 전부 추가
        return [...filteredMessages, ...newMessages];

      });

      // 디버그코드
      console.log("6. assistant 메시지 state 업데이트 완료");

      //로그인 상태일 떄만 ChatMessages 재조회 trigger
      if (currentRoom?.id) {

        setRefreshTrigger((prev) => prev + 1);

      }

    } catch (error) {

      console.log(error.response?.data);

    } finally {

      // AI 로딩 종료
      setIsLoading(false);

    }
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
        <textarea //여러 줄 입력 기능
          value={message}
          //메시지 창 크기 메시지에 따라 위로 크기 증가, 및 스크롤 추가
          onChange={(e) => {
            setMessage(e.target.value); 
            
            // 높이 초기화
            e.target.style.height = "auto";

            // 최대 높이 제한
            e.target.style.height =
              Math.min(e.target.scrollHeight, 220) + "px";
          }}
          placeholder="무엇을 배우고 싶나요?"

          // Enter 전송 / Shift+Enter 줄바꿈 
          onKeyDown={async (e) => {

            if (e.key === "Enter" && !e.shiftKey) {

              e.preventDefault();

              await handleSend();
            }
          }}

          rows={1}
          className="
            w-full
            bg-transparent
            outline-none
            resize-none
            overflow-y-auto
            max-h-[220px]

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
            //현재 dropdown 이 어떤 값을 보여줄지 결정하는 코드
            value={studyMode}

            //사용자가 dropdown 변경 시, studyMode state 변경하는 코드.
            onChange={(e) => setStudyMode(e.target.value)}

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