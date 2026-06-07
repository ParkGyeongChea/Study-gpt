//auth.js

// 서버 요청 담당 파일 토큰 저장/조회 삭제
// 브라우저 토큰 관리 담당 로컬스토리지 저장, 가져오기 삭제.
// 로컬스토리지 안에 저장하면 새로 고침해도 로그인 유지 등..



// 토큰 저장 함수 saveToken 생성
export const saveToken = (token) => {

  localStorage.setItem("token", token);
  
};

// 저장된 토큰 가져오기 함수 (로그인 상태 확인,API 요청,자동 로그인 유지 전부 토큰 필요)
export const getToken = () => {
  return localStorage.getItem("token");
};

// 토큰 삭제 함수 (로그아웃)
export const removeToken = () => {
  localStorage.removeItem("token");
  
};