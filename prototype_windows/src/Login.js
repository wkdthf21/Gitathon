import React from 'react';
import './Login.css'

function Login ({gitathonLogo, hackNum, teamNum}){
    return (
      <table className = "LoginMain">
          <tr>
              <td className = "LogoIcon">
                  <ShowLogo logoPath = {gitathonLogo} name = {"gitathonLogo"}/>
              </td>
          </tr>
          <tr>
              <td className = "Intro">
                  <Welcome hackNum = {hackNum} teamNum = {teamNum} />
              </td>
          </tr>
          <tr>
              <td className = "InputID">
                  <input type="text" name = "inputID"/>
              </td>
          </tr>
          <tr>
              <td className = "InputPW">
                  <input type="text" name = "inputPW"/>
              </td>
          </tr>
          <tr>
              <td className = "LoginBtn">
                  <button>함께하기</button>
              </td>
          </tr>
          <tr>
              <td className = "Join">
                  <div>
                      아직 계정이 없으신가요?
                       <font color = "red"> 회원가입 </font>
                  </div>
              </td>
          </tr>
      </table>
    )
}

function ShowLogo({logoPath, name}) {
    return(
      <img src = {logoPath} className = {name} alt ={name}/>
    )
}

function Welcome({hackNum, teamNum}){
  return(
    <span className = "Welcoming">
      현재 <font color = "red">{hackNum}</font>개
      의 해커톤과 <font color = "red">{teamNum}</font>개
      의 팀프로젝트가 진행중입니다.
    </span>
  )
}

export default Login;
