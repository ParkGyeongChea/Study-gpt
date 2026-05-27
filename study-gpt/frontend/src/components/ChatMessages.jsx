//ChatMessages.jsx

// 현재 선택한 room의 이전 대화 출력 컴포넌트


// React 기본 기능 import
//useRef = 특정 HTML 위치 기억하는 리액트 기능
import { useEffect, useRef, useState } from "react";

//react markdown 기능 추가
import ReactMarkdown from "react-markdown";

//incide-react에서 복사 아이콘 복사 완료 체크 아이콘 가져옴
import { Copy, Check } from "lucide-react";

//SyntaxHighlighter = 코드블럭 꾸며서 출력하는 컴포넌트
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";

//oneDark = GPT 느낌 나는 다크 테마 스타일
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

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

  // 복사 , 복사 완료 상태 추가
  const [copied, setCopied] = useState(false);

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

            animate-messageFade
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

            <div className="
              flex
              flex-col
              items-end
              gap-3

              max-w-[85%]
            ">

              {/* 업로드 파일 카드 */}
              {message.files?.length > 0 && (

                <div className="flex flex-col gap-2 w-full items-end">

                  {message.files.map((file, index) => (

                    <div
                      key={index}

                      className="
                        flex
                        items-center
                        gap-3

                        bg-zinc-900
                        border
                        border-zinc-700

                        rounded-2xl

                        px-4
                        py-3

                        min-w-[260px]
                        max-w-[320px]

                        shadow-md
                      "
                    >

                      {/* 파일 아이콘 */}
                      <div className="
                        w-10
                        h-10

                        rounded-xl

                        bg-red-500

                        flex
                        items-center
                        justify-center

                        text-white
                        text-lg
                      ">
                        📄
                      </div>

                      {/* 파일 정보 */}
                      <div className="flex-1 min-w-0">

                        <div className="
                          text-sm
                          font-semibold
                          text-white

                          truncate
                        ">
                          {file.name}
                        </div>

                        <div className="
                          text-xs
                          text-zinc-400
                        ">
                          PDF
                        </div>

                      </div>

                    </div>

                  ))}

                </div>

              )}

              {/* 실제 사용자 메시지 */}
              <div
                className="
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

            </div>

          ) : (

            /* AI 메시지 */
            <div
              className="
                w-full
                max-w-4xl
                text-black
                dark:text-white
                leading-8
                prose
                prose-invert
                prose-p:my-6
                prose-headings:mt-10
                prose-headings:mb-6
                prose-h1:text-3xl
                prose-h1:font-bold
                prose-h2:text-2xl
                prose-h2:font-bold
                prose-h3:text-xl
                prose-h3:font-semibold
                prose-headings:border-b
                prose-headings:border-zinc-800
                prose-headings:pb-3
                prose-strong:text-white
                prose-li:my-2
                prose-pre:rounded-2xl
                prose-pre:p-0
              "
            >

              {(() => {

                let parsedContent = null;

                // JSON parse 시도
                try {

                  parsedContent = JSON.parse(message.content);

                } catch {

                  parsedContent = null;
                }

                // =========================
                // quiz 타입 메시지
                // =========================

                if (parsedContent?.type === "quiz") {

                  return (

                    <div className="space-y-10">

                      {parsedContent.quiz.map((quiz, index) => (

                        <div key={index}>

                          <hr className="border-zinc-700 mb-8" />

                          <h2 className="text-3xl font-bold mb-10">
                            📝 학습 확인 퀴즈 {index + 1}
                          </h2>

                          <p className="mb-10 text-xl leading-10">
                            {quiz.question}
                          </p>

                          <div className="space-y-8">

                            {quiz.choices.map((choice, choiceIndex) => (

                              <div
                                key={choiceIndex}
                                className="text-lg leading-9"
                              >
                                ({choiceIndex + 1}) {choice}
                              </div>

                            ))}

                          </div>

                        </div>

                      ))}

                    </div>

                  );
                }

                // =========================
                // quiz_result 타입 메시지
                // =========================

                if (parsedContent?.type === "quiz_result") {

                  return (
                    <div className="space-y-8">
                      <hr className="border-zinc-700 mb-8" />
                      <h2 className="text-3xl font-bold mb-10">
                        📘 퀴즈 풀이 결과
                      </h2>

                      <ReactMarkdown>
                        {parsedContent.content}
                      </ReactMarkdown>
                    </div>
                  );
                }

                // =========================
                // 일반 markdown 메시지
                // =========================

                return (

                  <ReactMarkdown
                    components={{
                      code({ inline, className, children, ...props }) {

                        const match = /language-(\w+)/.exec(className || "");

                        return !inline && match ? (

                          <div className="relative">

                            <div
                              className="
                                absolute
                                top-3
                                left-3
                                flex
                                items-center
                                gap-2
                                px-3
                                py-1
                                rounded-md
                                bg-black/30
                                backdrop-blur-sm
                                text-zinc-200
                                text-xs
                                font-bold
                                tracking-wide
                                z-10
                              "
                            >
                              <span>{"</>"}</span>
                              <span>
                                {match[1]}
                              </span>
                            </div>

                            <button

                              onClick={() => {
                                navigator.clipboard.writeText(
                                  String(children).replace(/\n$/, "")
                                );

                                setCopied(true);

                                setTimeout(() => {
                                  setCopied(false);
                                }, 1500);

                              }}

                              className="
                                absolute
                                top-3
                                right-3

                                text-xs

                                bg-zinc-700
                                hover:bg-zinc-600

                                text-white

                                w-8
                                h-8

                                flex
                                items-center
                                justify-center

                                rounded-lg

                                transition
                              "
                            >
                              <span className="text-lg">
                                {copied ? (
                                  "✅"
                                ) : (
                                  <Copy size={18} />
                                )}
                              </span>

                            </button>

                            <SyntaxHighlighter
                              style={oneDark}
                              language={match[1]}
                              PreTag="div"
                              customStyle={{
                                borderRadius: "16px",
                                paddingTop: "52px",
                                paddingRight: "20px",
                                paddingBottom: "20px",
                                paddingLeft: "20px",
                                marginTop: "16px",
                                marginBottom: "16px",
                                fontSize: "15px"
                              }}
                              {...props}
                            >
                              {String(children).replace(/\n$/, "")}
                            </SyntaxHighlighter>

                          </div>

                        ) : (

                          <code
                            className="bg-zinc-800 px-1 py-0.5 rounded"
                            {...props}
                          >
                            {children}
                          </code>

                        );
                      }
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>

                );

              })()}

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