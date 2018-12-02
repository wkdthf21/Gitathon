import React, {Component} from 'react';
import { Button } from 'reactstrap';

class LoginMain extends Component{
    state={
        mode: 'Login'
    }

    render(){
        return(
            <div className="LoginScreen">
            if this.state.mode == 'Login'{
                <Login
                    gitathonLogo = {this.props.gitathonLogo}
                    hackNum = {this.props.numHack}
                    teamNum = {this.props.numTeam} />
            }
            else if {
                <Register />
            }
            </div>
        );
    }
}

class Login extends Component{
    constructor(props){
        super(props);
    }

    render(){
        return (
            <div class = "container">
            <form class="" action="/accounts/login" method="POST">

                <div class = "row">
                    <div class = "col-2">
                    </div>
                    <div class = "col-8">
                        <table className = "LoginMain">
                            <tr>
                                <td className = "LogoIcon">
                                    <ShowLogo logoPath = {this.props.gitathonLogo} name = {"gitathonLogo"}/>
                                </td>
                            </tr>
                            <tr>
                                <td className = "Intro">
                                    <Welcome hackNum = {this.props.hackNum} teamNum = {this.props.teamNum} />
                                </td>
                            </tr>
                            <tr>
                                <td className = "InputID">
      	    	                    <input type="text" name="memberId" placeholder="아이디를 입력해주세요" /><br />
                                </td>
                            </tr>
                            <tr>
                                <td className = "InputPW">
      		                        <input type="password" name="password" placeholder="비밀번호를 입력해주세요" /><br />
                                </td>
                            </tr>
                            <tr>
                                <td className = "LoginBtn">
                                    <input type="submit" name="" value="함께하기" />
                                </td>
                            </tr>
                            <tr>
                                <td className = "Join">
                                    <div>
                                        아직 계정이 없으신가요?
                                        <Button color = "danger" onclick="regBtnClick();">회원가입</Button>
                                    </div>
                                </td>
                            </tr>
                        </table>
                    </div>
                <div class = "col-2">
                </div>
            </div>
            </form>
        </div>
        );
    }

    regBtnClick(){
        this.setState({
            mode: "Register"
        });
    }
}

class Register extends Component{
    render(){
        return(
            <div class = "container">
                <Button onclick="finBtnClick();">완료</Button>
            </div>
        );
    }

    finBtnClick(){
        this.setState({
            mode: "Login"
        });
    }
}

function ShowLogo({logoPath, name}) {
    return(
      <img src = {logoPath} className = {name} alt ={name}/>
    )
}

function Welcome({hackNum, teamNum}){
  return(
    <span className = "Welcoming">
      현재  <font color = "red">{hackNum}</font>개의
      해커톤과 <font color = "red">{teamNum}</font>개의
      팀프로젝트가 진행중입니다.
    </span>
  )
}

export default Login;
