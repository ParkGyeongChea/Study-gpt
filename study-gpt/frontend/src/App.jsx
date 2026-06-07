//App.jsx

//React 전체 앱의 시작 구조를 만드는 파일
//실제 화면 구조를 결정하는 파일

import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ChatPage from "./pages/ChatPage"; 
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
