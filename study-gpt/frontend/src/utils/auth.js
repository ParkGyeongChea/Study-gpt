//auth.js

// 서버 요청 담당 파일 토큰 저장/조회 삭제
// 브라우저 토큰 관리 담당 로컬스토리지 저장, 가져오기 삭제.
// 로컬스토리지 안에 저장하면 새로 고침해도 로그인 유지 등..



// 토큰 저장 함수 saveToken 생성
export const saveToken = (token) => {
    //export = 다른 파일에서도 사용 가능하게 내보냄
    //화살표 함수, ()는 이 함수가 받을 값 저장할 토큰 문자열 받기 , token

  localStorage.setItem("token", token);
  //브라우저 저장 공간 객체인 localstroage에 setitem(데이터 저장) , token이라는 이름으로 실제 토큰값 저장
};

// 저장된 토큰 가져오기 함수 (로그인 상태 확인,API 요청,자동 로그인 유지 전부 토큰 필요)
export const getToken = () => {
  return localStorage.getItem("token");
  //token 이름으로 getitem(저장된 데이터 가져오기) 저장된 토큰값 반환
};

// 토큰 삭제 함수 (로그아웃)
export const removeToken = () => {
  localStorage.removeItem("token");
  //저장된 데이터 삭제, token 이름의 데이터 삭제
};