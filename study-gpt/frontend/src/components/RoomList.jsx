//RoomList.jsx

// 왼쪽 채팅방 목록 전용 파일


// React 기본 기능 import
import { useEffect, useState } from "react";
// useState = 값 저장용 state 기능
// useEffect = 화면 시작 시 자동 실행 기능


// backend API 요청 객체 import
import api from "../api/api";
// api.js 파일의 axios 객체 가져오기
// 이제 backend API 요청 가능


// RoomList 컴포넌트
// 부모(ChatPage)에게 setSelectedRoom 함수 전달받음
export default function RoomList({ setSelectedRoom }) {


  // 채팅방 목록 저장 state
  const [rooms, setRooms] = useState([]);
  // rooms = room 목록 저장 변수
  // setRooms = room 목록 변경 함수
  // [] = 처음엔 빈 배열


  // 화면 시작 시 자동 실행
  useEffect(() => {

    // room 목록 요청 함수 실행
    fetchRooms();

  }, []);
  // [] = 처음 1번만 실행


  // backend room 목록 요청 함수
  const fetchRooms = async () => {

    // GET /rooms 요청
    const response = await api.get("/rooms");
    // backend의 /rooms API 호출
    // await = 응답 올 때까지 기다림


    // 응답 데이터를 rooms state에 저장
    setRooms(response.data);
    // response.data 안에 room 목록 들어있음
    // rooms state 변경 시 화면 자동 업데이트
  };


  return (

    <div>

      {/* room 배열 반복 출력 */}
      {rooms.map((room) => (
      // rooms 배열 하나씩 반복 출력
      // room 안에는 id/title 같은 데이터 들어있음

        <div
          key={room.id}
          // React 반복 출력용 고유값
          // key 없으면 React가 목록 구분 못함

          onClick={() => setSelectedRoom(room)}
          // room 클릭 시 실행
          // 현재 room 데이터를 부모(ChatPage) state에 저장

          className="p-3 border-b cursor-pointer hover:bg-gray-100"
          // p-3 = 안쪽 여백
          // border-b = 아래쪽 테두리
          // cursor-pointer = 마우스 올리면 클릭 모양
          // hover:bg-gray-100 = 마우스 올리면 배경색 변경
        >

          {/* room 제목 출력 */}
          {room.title}

        </div>

      ))}

    </div>
  );
}