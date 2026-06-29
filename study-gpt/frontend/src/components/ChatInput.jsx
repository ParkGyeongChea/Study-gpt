//ChatInput.jsx
// 입력창 + 메시지 전송 담당 컴포넌트



import { useRef, useState } from "react";
import api from "../api/api";


// ChatInput 컴포넌트
export default function ChatInput({

  selectedRoom,
  setSelectedRoom,
  setRoomRefreshTrigger,
  setRefreshTrigger,
  messages,
  setMessages,
  isLoading,
  setIsLoading,
  studyMode,
  setStudyMode

}) {

  // 입력창 값 저장 state
  const [message, setMessage] = useState("");

  // 업로드 파일 state
  const [uploadedFiles, setUploadedFiles] = useState([]);

  // 숨겨진 파일 input 접근용 ref
  const fileInputRef = useRef(null);

  // 파일 업로드 처리
  
  // 파일 drag & drop 처리
  const handleDrop = (e) => {

    e.preventDefault();

    const files = Array.from(e.dataTransfer.files);

    setUploadedFiles((prev) => [
      ...prev,
      ...files
    ]);
  };


  // drag 중 기본 이벤트 방지
  const handleDragOver = (e) => {

    e.preventDefault();

  };


  // 업로드 파일 제거
  const removeFile = (indexToRemove) => {

    setUploadedFiles((prev) =>
      prev.filter((_, index) =>
        index !== indexToRemove
      )
    );
  };

  // + 버튼으로 파일 선택 처리
  const handleFileSelect = (e) => {

    const files = Array.from(e.target.files);

    setUploadedFiles((prev) => [
      ...prev,
      ...files
    ]);

    e.target.value = "";
  };

  
  // 메시지 전송 함수

  const handleSend = async () => {
    
    // 공백 입력 방지
    if (!message.trim()) return;

    // user 메시지 즉시 화면 출력
    const tempMessage = {
      id: Date.now(),
      role: "user",
      content: message,

      // 업로드 파일 정보 저장
      files: uploadedFiles.map((file) => ({
        name: file.name,
        type: file.type
      }))
    };

    
    setMessage("");
    setMessages((prev) => [...prev, tempMessage]);
    let currentRoom = selectedRoom;
    const token = localStorage.getItem("token");


    // room 없는 경우, 로그인 상태일 떄만 생성
    if (!currentRoom && token) {
      const roomResponse = await api.post("/rooms", {
        title: "새 채팅"
      });

      currentRoom = roomResponse.data;
      setSelectedRoom(currentRoom);
      setRoomRefreshTrigger((prev) => prev + 1);
      setMessages((prev) => [...prev]);
    }


    
    // AI 로딩 시작
    
    setIsLoading(true);

    if (currentRoom?.id) {
      setRoomRefreshTrigger((prev) => prev + 1);
    }


    const loadingMessage = {
      id: "loading",
      role: "assistant",
      content: "답변 생성 중..."
    };
    

    setMessages((prev) => [...prev,loadingMessage]);


    // FormData 생성
   
    const formData = new FormData();

    formData.append(
      "message",
      message
    );

    formData.append(
      "study_mode",
      studyMode
    );


    // room_id 존재 시 추가
    if (currentRoom?.id) {

      formData.append(
        "room_id",
        currentRoom.id
      );
    }

    // 업로드 파일 추가
    uploadedFiles.forEach((file) => {

      formData.append(
        "files",
        file
      );

    });

    // 전송 즉시 업로드 preview 제거
    setUploadedFiles([]);

    
    try {
      const response = await api.post(
        "/agent",
        formData,
        {
          headers: {
            "Content-Type":
              "multipart/form-data"
          }
        }

      );

      const responseType = response.data?.type;

      console.log("응답 타입:", responseType);

      setRoomRefreshTrigger((prev) => prev + 1);
      
      const newMessages = [];

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
        const filteredMessages = prev.filter(
          (msg) => msg.id !== "loading"
        );

        
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



  // 화면 출력(UI)
 
  return (

    <div className="mt-6" onDrop={handleDrop} onDragOver={handleDragOver}>

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

        {/* 업로드 파일 미리보기 */}
        {uploadedFiles.length > 0 && (

          <div className="
            flex
            gap-3
            mb-4
            flex-wrap
          ">

            {uploadedFiles.map((file, index) => (

              <div
                key={index}

                className="
                  relative
                  bg-zinc-800
                  border
                  border-zinc-700
                  rounded-2xl
                  px-4
                  py-3
                  text-sm
                  text-white
                  min-w-[120px]
                  max-w-[220px]
                "
              >

                {/* 제거 버튼 */}
                <button
                  onClick={() => removeFile(index)}

                  className="
                    absolute
                    -top-2
                    -right-2

                    w-6
                    h-6

                    rounded-full
                    bg-white
                    text-black
                    text-xs
                    font-bold
                  "
                >
                  ✕
                </button>

                {/* 파일 이름 */}
                <div className="truncate">
                  {file.name}
                </div>

              </div>

            ))}

          </div>

        )}

        {/* 실제 메시지 입력창 */}
        <textarea 
          value={message}
          onChange={(e) => {
            setMessage(e.target.value); 
            e.target.style.height = "auto";
            e.target.style.height =
              Math.min(e.target.scrollHeight, 220) + "px";
          }}
          placeholder="무엇을 배우고 싶나요?"

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


        {/* 아래 버튼 영역 */}
        <div className="flex justify-between items-center mt-4">

          {/* 숨겨진 파일 선택 input */}
          <input
            ref={fileInputRef}
            type="file"
            multiple
            onChange={handleFileSelect}
            className="hidden"
          />

          {/* 첨부파일 버튼 */}
          <button
            type="button"
            onClick={() => {
              fileInputRef.current?.click();
            }}
            className="
              w-10 h-10
              bg-transparent
              text-white
              text-4xl
              leading-none
              flex items-center justify-center
              hover:text-zinc-300
              transition
            "
          >
            +
          </button>

          <div className="flex items-center gap-3">

            {/* 새 학습 시작 전일 때만 학습 모드 표시 */}
            {!selectedRoom && (
              <select
                value={studyMode}
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
                <option value="free">자유 학습</option>
                <option value="light_quiz">가벼운 확인</option>
                <option value="strict_quiz">집중 학습</option>
              </select>
            )}

            {/* 전송 버튼 */}
            <button
              type="button"
              onClick={handleSend}
              disabled={isLoading || !message.trim()}
              className="
                w-11 h-11
                rounded-full
                bg-blue-500
                text-white
                flex items-center justify-center
                text-2xl
                font-bold
                leading-none
                hover:bg-blue-600
                disabled:opacity-40
                disabled:cursor-not-allowed
                transition
              "
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.3"
                className="w-7 h-7"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 18V6"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M8.5 9.5L12 6l3.5 3.5"
                />
</svg>
            </button>

          </div>
        </div>

      </div>

    </div>

  );
}