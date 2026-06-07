//RoomList.jsx

// 왼쪽 채팅방 목록 전용 파일



import { useEffect, useRef, useState } from "react";
import api from "../api/api";
import { getToken, removeToken } from "../utils/auth";
import SettingsModal from "./SettingsModal";
import { useNavigate } from "react-router-dom";


// RoomList 컴포넌트 props
export default function RoomList({
  setSelectedRoom,
  setMessages,
  setIsSidebarOpen,
  selectedRoom,
  isSidebarOpen,
  roomRefreshTrigger

}) {
  
  const navigate = useNavigate();
  const [showSidebarContent, setShowSidebarContent] = useState(isSidebarOpen);
  const [contextMenu, setContextMenu] = useState(null);
  const [deleteRoomId, setDeleteRoomId] = useState(null);
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isSettingsModalOpen, setIsSettingsModalOpen] = useState(false);
  const profileMenuRef = useRef(null);
  const contextMenuRef = useRef(null);
  

  useEffect(() => {
    if (isSidebarOpen) {
      const timer = setTimeout(() => {
        setShowSidebarContent(true);
      }, 140);

      return () => clearTimeout(timer);
    }
    setShowSidebarContent(false);
  }, [isSidebarOpen]);

  useEffect(() => {

  // ESC 키 처리
  const handleEsc = (e) => {
    if (e.key === "Escape") {
      setIsProfileMenuOpen(false);
    }
  };


  // 바깥 클릭 처리
  const handleClickOutside = (e) => {
    if (
      profileMenuRef.current &&
      !profileMenuRef.current.contains(e.target)
    ) {
      setIsProfileMenuOpen(false); 
    }

    if (
    contextMenuRef.current &&
    !contextMenuRef.current.contains(e.target) 
  ) {
    setContextMenu(null);
  }
    
  };

  window.addEventListener("keydown", handleEsc);
  window.addEventListener("mousedown", handleClickOutside);

  return () => {
    window.removeEventListener("keydown", handleEsc);
    window.removeEventListener("mousedown", handleClickOutside);
  };
}, []);


  // 메인 화면 이동 함수
  const goToHome = () => {
    setSelectedRoom(null);
    setMessages([]);
  };

  const token = getToken();
  const email = localStorage.getItem("email");
  const isLoggedIn = token && email;

  // 로그아웃 함수
  const handleLogout = () => {
    removeToken();
    localStorage.removeItem("email");
    window.location.reload();

  };


  const [rooms, setRooms] = useState([]);
  const [editingRoomId, setEditingRoomId] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [showArchive, setShowArchive] = useState(true);
  const [expandedRooms, setExpandedRooms] = useState({});
  const [draggedRoomId, setDraggedRoomId] = useState(null);
  const [hoveredRoomId, setHoveredRoomId] = useState(null);

  // 현재 진행중인 학습 room만 분리
  const activeRooms = rooms.filter(
    (room) => room.is_archived === false
  );

  // 최상위 room만 추출
  const rootRooms = activeRooms.filter(
    (room) => room.parent_room_id === null
  );

  // 특정 room의 자식 room 찾기
  const getChildRooms = (parentId) => {

    return activeRooms.filter(
      (room) => room.parent_room_id === parentId
    );

  };

  // 특정 room의 모든 하위 자식 검사 함수
  const isChildRoom = (parentId, targetId) => {

    const children = rooms.filter(
      (room) => room.parent_room_id === parentId
    );


    for (const child of children) {

   
      if (child.id === targetId) {
        return true;
      }


      if (isChildRoom(child.id, targetId)) {
        return true;
      }

    }

    return false;

  };

  // room 펼치기/접기 토글 함수
  const toggleRoomExpand = (roomId) => {

    setExpandedRooms((prev) => ({
      ...prev,

      [roomId]: !prev[roomId]

    }));

  };

  // 재귀 room 렌더링 함수
  const renderRoom = (room, depth = 0) => {

    return (

      <div key={room.id}>

        {/* 현재 room */}
        <div
          draggable 
          onDragStart={() => { 
            setDraggedRoomId(room.id); 
          }}

          onDragEnd={() => {
            setHoveredRoomId(null);
            setDraggedRoomId(null);
          }}
          
          onDragOver={(e) => {
            e.preventDefault();
            setHoveredRoomId(room.id);

          }}
          onDrop={async () => {

            if (draggedRoomId === room.id) {
              return;
            }

            if (isChildRoom(draggedRoomId, room.id)) {
              return;
            }

            try {
              await api.put(
                `/rooms/${draggedRoomId}/parent`,
                {
                  parent_room_id: room.id 
                }
              );
              
              fetchRooms();
              setHoveredRoomId(null);
              setDraggedRoomId(null);

            } catch (error) {
              console.log(error);
            }
          }}
          onClick={() => {
            setSelectedRoom(room);
            setMessages([]);
          }}

          onContextMenu={(e) => {

            e.preventDefault();

            setContextMenu({
              x: e.clientX,
              y: e.clientY,
              roomId: room.id,
              isArchived: room.is_archived
            });

          }}

          className={`
            ${depth === 0 ? "mt-2 p-3" : "mt-1 py-1 px-2"}

            cursor-pointer
            transition-all duration-200
            text-black
            dark:text-white

            
            ${
              selectedRoom?.id === room.id
                ? `
                  bg-gray-300
                  dark:bg-zinc-800
                  rounded-xl
                  font-semibold
                `
                : `
                  hover:bg-gray-200
                  dark:hover:bg-zinc-900
                  hover:rounded-xl
                `
            }
          `}

          style={{
            marginLeft: `${depth * 24}px`
          }}
        >

          <div className="flex items-center gap-3">

            {selectedRoom?.id === room.id && (

              <div
                className="
                  w-1
                  h-6
                  rounded-full
                  bg-blue-500
                "
              />

            )}
              {/* 자식 room 존재 시 펼치기 버튼 */}
              {getChildRooms(room.id).length > 0 && (
                <button
                  onClick={(e) => {
                    e.stopPropagation(); 
                    toggleRoomExpand(room.id);
                  }}
                  className="
                    text-xs
                    text-zinc-400
                    hover:text-white
                    transition
                  "
                >
                  {expandedRooms[room.id] ? "▼" : "▶"}
                </button>
              )}
            <span>
              {depth > 0 && "└ "}
              {room.title}
            </span>
          </div>
        </div>
        {/* 현재 hover 중인 room insertion line */}
        {
          hoveredRoomId === room.id &&
          draggedRoomId &&
          draggedRoomId !== room.id && (

          <div
            className="
              h-[2px]
              bg-blue-500
              rounded-full
              ml-6
              mr-2
              opacity-80
            "
          />

        )}

        {/* 펼쳐진 room만 자식 출력 */}
        {expandedRooms[room.id] && (
          getChildRooms(room.id).map((childRoom) => (
            renderRoom(childRoom, depth + 1)
          ))
        )}
      </div>
    );
  };


  const archivedRooms = rooms.filter(
    (room) => room.is_archived === true
  );


  const archivedRootRooms = archivedRooms.filter(
    (room) => room.parent_room_id === null
  );


  const getArchivedChildRooms = (parentId) => {

    return archivedRooms.filter(
      (room) => room.parent_room_id === parentId
    );

  };

  const renderArchivedRoom = (room, depth = 0) => {
    return (
      <div key={room.id}>

        <div
          draggable

          onDragStart={() => {
            setDraggedRoomId(room.id);
          }}

          onDragEnd={() => {
            setHoveredRoomId(null);
            setDraggedRoomId(null);
          }}

          onDragOver={(e) => {
            e.preventDefault();
            setHoveredRoomId(room.id);
          }}

          onDrop={async () => {
            if (draggedRoomId === room.id) {
              return;
            }

            if (isChildRoom(draggedRoomId, room.id)) {
              return;
            }

            try {
              await api.put(
                `/rooms/${draggedRoomId}/parent`,
                {
                  parent_room_id: room.id
                }
              );

              fetchRooms();

              setHoveredRoomId(null);
              setDraggedRoomId(null);

            } catch (error) {
              console.log(error);
            }
          }}

          onClick={() => {
            setSelectedRoom(room);
            setMessages([]);
          }}

          onContextMenu={(e) => {
            e.preventDefault();

            setContextMenu({
              x: e.clientX,
              y: e.clientY,
              roomId: room.id,
              isArchived: room.is_archived
            });
          }}

          className={`
            ${depth === 0 ? "mt-2 p-3" : "mt-1 py-1 px-2"}

            cursor-pointer
            transition-all duration-200
            text-black
            dark:text-white

            ${
              selectedRoom?.id === room.id
                ? `
                  bg-gray-300
                  dark:bg-zinc-800
                  rounded-xl
                  font-semibold
                `
                : `
                  hover:bg-gray-200
                  dark:hover:bg-zinc-900
                  hover:rounded-xl
                `
            }
          `}

          style={{
            marginLeft: `${depth * 24}px`
          }}
        >
          <div className="flex items-center gap-3">

            {getArchivedChildRooms(room.id).length > 0 && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  toggleRoomExpand(room.id);
                }}
                className="
                  text-xs
                  text-zinc-400
                  hover:text-white
                  transition
                "
              >
                {expandedRooms[room.id] ? "▼" : "▶"}
              </button>
            )}

            <span>
              {depth > 0 && "└ "}
              {room.title}
            </span>

          </div>
        </div>

        {hoveredRoomId === room.id &&
          draggedRoomId &&
          draggedRoomId !== room.id && (
            <div
              className="
                h-[2px]
                bg-blue-500
                rounded-full
                ml-6
                mr-2
                opacity-80
              "
            />
        )}

        {expandedRooms[room.id] && (
          getArchivedChildRooms(room.id).map((childRoom) => (
            renderArchivedRoom(childRoom, depth + 1)
          ))
        )}

      </div>
    );
  };
  
  // 화면 시작 시 자동 실행
  useEffect(() => {
    const token = getToken();
    if (!token) return;
    fetchRooms();
  }, [roomRefreshTrigger]);

  // backend room 목록 요청 함수
  const fetchRooms = async () => {
    const response = await api.get("/rooms");
    setRooms(response.data);
  };
  return (


    // 전체 사이드바 영역
    <div className="flex flex-col h-full">


      {/* =========================
          상단 헤더 영역
      ========================= */}

      {showSidebarContent && (

        <div className="mb-4 space-y-3">

          {/* 로고 영역 */}
          <div className="flex justify-start pl-[20px]">

            <h1
              onClick={goToHome}
              className="
                text-4xl
                font-extrabold
                cursor-pointer
                text-black
                dark:text-white
              "
            >
              Study GPT
            </h1>

          </div>


          {/* 새 채팅 버튼 */}
          <button
            onClick={goToHome}
            className="
              w-full
              bg-blue-500
              text-white
              p-3
              rounded
            "
          >
            + 새 채팅
          </button>

        </div>

      )}


      {/* =========================
          채팅방 목록 영역
      ========================= */}

      {showSidebarContent ? (

        isLoggedIn && (

          <div className="flex-1 overflow-y-auto">

          {/* 현재 학습 섹션 */}
          <div
            className={`
              mb-6
              min-h-[220px]
              pb-12
              rounded-2xl
              transition-all duration-200
            `}

            onDragOver={(e) => {
              e.preventDefault();
            }}
            onDrop={async () => {

              // 드래그 room 없으면 종료
              if (!draggedRoomId) {
                return;
              }
              try {

              // 현재 드래그 room 찾기
              const draggedRoom = rooms.find(
                (room) => room.id === draggedRoomId
              );

              // archive 상태면 active로 복귀
              if (draggedRoom?.is_archived) {

                await api.put(
                  `/rooms/${draggedRoomId}/archive`
                );

              }

              // 최상위 room으로 변경
              await api.put(
                `/rooms/${draggedRoomId}/parent`,
                {
                  parent_room_id: null
                }
              );

              // room 목록 다시 조회
              fetchRooms();

            } catch (error) {

              console.log(error);

            }
            }}
          >

            <div
              className="
                flex items-center
                gap-2
                text-base
                font-extrabold
                text-zinc-50
                mb-4
                px-2
                tracking-wide
              "
            >
              <span className="text-lg">
                📝
              </span>

              현재 학습
            </div>
            {/* 재귀 렌더링 시작점  */}
            {rootRooms.map((room) => (

              renderRoom(room)

            ))}
          </div>
          {/* 현재 학습 / 아카이브 구분선 */}
          <div
            className="
              border-t-2
              border-zinc-700
              my-6
            "
          />

          {/* 학습 아카이브 섹션 */}
          <div
            className={`
              mt-8
              min-h-[220px]
              pb-12
              rounded-2xl
              transition-all duration-200
            `}
            onDragOver={(e) => {
              e.preventDefault();
            }}
            
            onDrop={async () => {

              // 드래그 room 없으면 종료
              if (!draggedRoomId) {
                return;
              }

              // 현재 드래그중인 room 찾기
              const draggedRoom = rooms.find(
                (room) => room.id === draggedRoomId
              );

              // 이미 archive 상태면 종료
              if (draggedRoom?.is_archived) {
                return;
              }

              try {
                // archive 이동 요청
                await api.put(
                  `/rooms/${draggedRoomId}/archive`
                );

                // room 목록 다시 조회
                fetchRooms();

              } catch (error) {

                console.log(error);

              }

            }}
          >
            <div
              onClick={() => {
                setShowArchive(!showArchive);
              }}
              className="
                flex items-center
                justify-between
                cursor-pointer
                text-base
                font-extrabold
                text-zinc-50
                mb-4
                px-2
                tracking-wide
                hover:opacity-80
                transition
              "
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">
                  📁
                </span>
                학습 아카이브
              </div>
              <span className="text-sm text-zinc-400">
                {showArchive ? "▼" : "▶"}
              </span>
            </div>
              {showArchive && (
                <div
                  className="
                    mt-3
                  "
                >
                
                {[...archivedRootRooms]
                  .reverse()
                  .map((room) => (

                    renderArchivedRoom(room)

                ))}
            </div>
          )}
          </div>
        </div>
        )
      ) : (

        
        <div className="flex-1" />
      

      )}


      {/* 하단 계정 영역 */}
      <div
        className="
          border-t border-gray-300 dark:border-zinc-800
          mt-2
          p-4
        "
      >
        {/* 로그인 상태 */}
        {isLoggedIn ? (
          <div
            onClick={() => setIsProfileMenuOpen((prev) => !prev)}
            className="
              relative
              h-12
              w-full
              pl-2
              cursor-pointer
              group
            "
          >
            {/* 프로필 hover 배경 */}
            <div
              className={`
                absolute
                bg-transparent
                group-hover:bg-zinc-800
                transition

                ${isSidebarOpen
                  ? "left-[-15px] right-0 top-0 bottom-0 rounded-xl"
                  //사이드바 닫혔을때 hover 이펙트 크기 조절
                  : "left-[-21px] top-1/2 -translate-y-1/2 w-[57px] h-[57px] rounded-full"}
              `}
            />

            {/* 원형 프로필 */}
          <div
            className="
              absolute
              z-10
              left-[-15px]
              top-1/2
              -translate-y-1/2
              w-10 h-10
              rounded-full
              bg-blue-500
              flex items-center justify-center
              text-white
              font-bold
            "
          >
            {email?.charAt(0)?.toUpperCase()}
          </div>

          {/* 펼쳐졌을 때 계정 정보 */}
          <div
            className={`
              absolute
              z-10
              left-14
              top-1/2
              -translate-y-1/2
              flex flex-col
              transition-opacity duration-150

              ${isSidebarOpen && showSidebarContent
                ? "opacity-100"
                : "opacity-0 pointer-events-none"}
            `}
          >
            <div className="text-white text-sm font-semibold whitespace-nowrap">
              {email}
            </div>

            <div className="text-zinc-400 text-xs whitespace-nowrap">
              구독중
            </div>
          </div>
          {/* 프로필 메뉴 */}
          {isProfileMenuOpen && (
            <div
              ref={profileMenuRef}
              className="
                absolute
                bottom-14
                left-0
                w-52
                bg-zinc-900
                border border-zinc-700
                rounded-2xl
                shadow-xl
                p-2
                z-50
              "
            >
              {/* 설정 */}
              <button
                onClick={() => {
                  setIsProfileMenuOpen(false); 
                  setIsSettingsModalOpen(true); 
                }} 
                className="
                  w-full
                  text-left
                  px-4 py-3
                  rounded-xl
                  hover:bg-zinc-800
                  transition
                  text-white
                "
              >
                설정
              </button>

              {/* 로그아웃 */}
              <button
                onClick={handleLogout}
                className="
                  w-full
                  text-left
                  px-4 py-3
                  rounded-xl
                  hover:bg-zinc-800
                  transition
                  text-red-400
                "
              >
                로그아웃
              </button>

              
            </div>
          )}
          </div>
          
        ) : (
          <div className="relative h-20 w-full -mt-2">
            {/* 접힌 상태 아이콘 */}
            <div
              className={`
                absolute
                left-1/2
                top-1/2
                -translate-x-1/2
                -translate-y-1/2
                transition-opacity duration-150

                ${isSidebarOpen
                  ? "opacity-0 pointer-events-none"
                  : "opacity-100"}
              `}
            >
              <div
                onClick={() => navigate("/login")}
                className="
                  w-10 h-10
                  rounded-full
                  bg-zinc-600
                  flex items-center justify-center
                  cursor-pointer
                  hover:bg-zinc-500
                  transition
                "
              >
                {/* 파란색 사람 실루엣 아이콘 (text-blue-400으로 색상 제어) */}
                <svg 
                  xmlns="http://www.w3.org/2000/svg" 
                  viewBox="0 0 24 24" 
                  fill="currentColor" 
                  className="w-5 h-5 text-blue-400"
                >
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
            </div>

            {/* 펼친 상태 로그인/회원가입 버튼 */}
            <div
              className={`
                absolute
                left-0
                top-0
                w-full
                flex flex-col gap-2
                transition-opacity duration-150

                ${isSidebarOpen && showSidebarContent
                  ? "opacity-100"
                  : "opacity-0 pointer-events-none"}
              `}
            >
              <button
                onClick={() => navigate("/login")}
                className="
                  w-full
                  bg-zinc-800
                  hover:bg-zinc-700
                  text-white
                  p-2
                  rounded-lg
                  transition
                "
              >
                로그인
              </button>

              <button
                onClick={() => navigate("/signup")}
                className="
                  w-full
                  bg-white
                  hover:bg-gray-200
                  text-black
                  p-2
                  rounded-lg
                  transition
                "
              >
                회원가입
              </button>
            </div>
          </div>
        )}
      </div>
    {/* 우클릭 메뉴 ,우클릭 시에만 메뉴 표시*/}
    {contextMenu && (
      <div
        
        ref={contextMenuRef}
        style={{
          top: contextMenu.y,
          left: contextMenu.x
        }}

        className="
          fixed
          z-50
          w-40
          bg-zinc-900
          border border-zinc-700
          rounded-xl
          shadow-xl

          p-2
        "
      >

        {/* 채팅방 이동 버튼 */}
        <button
          onClick={async () => {

            try {

              // 현재 상태 반대로 변경
              await api.put(
                `/rooms/${contextMenu.roomId}/archive`,
                {
                  is_archived: !contextMenu.isArchived
                }
              );

              // room 목록 다시 조회
              fetchRooms();

              // 우클릭 메뉴 닫기
              setContextMenu(null);

            } catch (error) {

              console.log(error);

            }

          }}

          className="
            w-full
            text-left
            px-4 py-2
            rounded-lg
            hover:bg-zinc-800
            transition
            text-white
          "
        >
          {contextMenu.isArchived
            ? "현재 학습으로 이동"
            : "아카이브 이동"}
        </button>
        {/* 이름 변경 버튼 */}
        <button
          onClick={() => {

            // 현재 이 room 수정 시작 상태 저장
            setEditingRoomId(contextMenu.roomId);

            // 기존 제목 input에 미리 넣기, 현재 수정하려는 room 객체 찾기
            const targetRoom = rooms.find(
              (room) => room.id === contextMenu.roomId
            );

            setEditTitle(targetRoom.title);

            // 우클릭 메뉴 닫기
            setContextMenu(null);
          }}

          className="
            w-full
            text-left
            px-4 py-2
            rounded-lg
            hover:bg-zinc-800
            transition
            text-white
          "
        >
          이름 변경
        </button>

        {/* 삭제 버튼 */}
        <button
          onClick={() => {
            setDeleteRoomId(contextMenu.roomId); //삭제 확인창 열기
            setContextMenu(null); //우클릭 메뉴 닫기
          }}
          className="
            w-full
            text-left
            px-4 py-2
            rounded-lg
            hover:bg-zinc-800
            transition
            text-red-400
          "
        >
          삭제
        </button>
        

      </div>

    )}
    {/* 삭제 확인 모달 */}
    {deleteRoomId && (
      <div
        className="
          fixed inset-0
          z-50

          bg-black/60

          flex
          items-center
          justify-center
        "
      >

        {/* 모달 박스 */}
        <div
          className="
            w-[420px]
            bg-zinc-900
            rounded-2xl
            p-6
            border border-zinc-800
          "
        >

          {/* 제목 */}
          <h2
            className="
              text-2xl
              font-bold
              text-white
            "
          >
            채팅방을 삭제하시겠습니까?
          </h2>

          {/* 설명 */}
          <p
            className="
              mt-4
              text-zinc-300
              leading-7
            "
          >
            이 채팅방과 저장된 메시지가 삭제됩니다.
          </p>

          {/* 버튼 영역 */}
          <div
            className="
              flex
              justify-end
              gap-3
              mt-8
            "
          >

            {/* 취소 버튼 */}
            <button

              onClick={() => {
                setDeleteRoomId(null);
              }}

              className="
                px-5 py-2
                rounded-xl
                bg-zinc-800
                hover:bg-zinc-700
                text-white
                transition
              "
            >
              취소
            </button>

            {/* 삭제 버튼 */}
            <button
              onClick={async () => {
                try {
                  await api.delete(
                    `/rooms/${deleteRoomId}`
                  );
                  fetchRooms();

                  if (selectedRoom?.id === deleteRoomId) {
                    setSelectedRoom(null);
                    setMessages([]);
                  }

                  setDeleteRoomId(null);

                } catch (error) {
                  console.log(error);
                }

              }}

              className="
                px-5 py-2
                rounded-xl
                bg-red-500
                hover:bg-red-600
                text-white
                transition
              "
            >
              삭제
            </button>

          </div>

        </div>

      </div>

    )}
    {/* 설정창 */}
    {isSettingsModalOpen && (
      <SettingsModal
        onClose={() => setIsSettingsModalOpen(false)}
      />
    )}
    </div>
  );
}