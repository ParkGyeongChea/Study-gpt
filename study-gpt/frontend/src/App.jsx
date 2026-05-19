//App.jsx

//React 전체 앱의 시작 구조를 만드는 파일
//실제 화면 구조를 결정하는 파일

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
//react-router-dom 라이브러리에서 페이지 이동에 필요한 기능들을 가져오는 코드.
//BrowserRouter : 주소 기반 페이지 이동 기능을 켜는 큰 박스
//Routes : 여러 라우터들을 묶는 영역
//Route : 특정 주소와 특정 페이지를 연결
//Navigate : 강제로 다른 주소로 이동

import ChatPage from "./pages/ChatPage"; //chatpage 컴포넌트 가져오기
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";


function App() {
  return (
    <BrowserRouter>
      <Routes>
      
        <Route path="/"element={<ChatPage />}/>
        {/* 메인 채팅 화면은 누구나 들어올 수 있음 */}

        <Route path="/login" element={<LoginPage />} /> 
        {/* 주소가 /login이면 loginpage를 보여줌 */}

        <Route path="/signup" element={<SignupPage />} />
        {/* 주소가 /signup 이면 signuppage를 보여줌 */}
    
        <Route path="*" element={<Navigate to="/" replace />} />
        {/* 존재하지 않는 주소로 들어오면 / 로 보내는 코드 */}

      </Routes>
    </BrowserRouter>
  );
}

export default App; // main.jsx에서 App 사용 가능
