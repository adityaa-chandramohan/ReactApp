import React from 'react';

const initialState = {
  ip: '',
  lastaccessed: ''
}


class LoginInfo extends React.Component {

  constructor(props) {
    super(props);
    this.state=initialState;
  }

  componentDidMount(){
      fetch('http://localhost:5000/api/login_attempt/'+this.props.id, {
      method: 'get',
      headers: {'Content-Type': 'application/json'}
    })
      .then(response => response.json())
      .then(loginInfo => {
        if (loginInfo.id) {
          this.setState({ip:loginInfo.ip});
          this.setState({lastaccessed:loginInfo.lastaccessed});
        }
      })
  }

  render() {
    return(
      <div>
        <div className='center'>
          <div>
            You logged in from {this.state.ip} at {this.state.lastaccessed}
          </div>
        </div>
      </div>
    );
}

}


export default LoginInfo;
