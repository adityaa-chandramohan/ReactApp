import React from 'react';

const initialState = {
  signInEmail: '',
  signInPassword: '',
  emailError: '',
  passwordError: ''
}

const errorState={
  emailError: '',
  passwordError: ''
}

class Signin extends React.Component {

  constructor(props) {
    super(props);
    this.state = initialState
  }

  onEmailChange = (event) => {
    this.setState({signInEmail: event.target.value})
  }

  onPasswordChange = (event) => {
    this.setState({signInPassword: event.target.value})
  }

  validate = () => {
   let emailError = "";
   let passwordError = "";

   if(!this.state.signInEmail.includes("@")){
     emailError = "invalid email";
   }

   if(!this.state.signInPassword){
     passwordError = "password field cannot be blank.";
   }

   if(emailError || passwordError)
   {
     this.setState({emailError,passwordError})
     return false;
   }

   return true;
 };

  onSubmitSignIn = () => {
    const isValid = this.validate()

    if(isValid){
      fetch('http://localhost:5000/api/login', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email: this.state.signInEmail,
        password: this.state.signInPassword
      })
    })
      .then(response => response.json())
      .then(user => {
        if (user.id) {
          this.props.loadUser(user)
          this.props.onRouteChange('home');
        }
      })
      .catch((error) => {
      this.setState({ passwordError: "Username or password is incorrect."})
      })

      this.setState(errorState)
    }
  }

  render() {
    const { onRouteChange } = this.props;
    return (
      <article className="br3 ba b--black-10 mv4 w-100 w-50-m w-25-l mw6 shadow-5 center">
        <main className="pa4 black-80">
          <div className="measure">
            <fieldset id="sign_up" className="ba b--transparent ph0 mh0">
              <legend className="f1 fw6 ph0 mh0">Sign In</legend>
              <div className="mt3">
                <label className="db fw6 lh-copy f6" htmlFor="email-address">Email</label>
                <input
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="email"
                  name="email-address"
                  id="email-address"
                  onChange={this.onEmailChange}
                />
              </div>
              <div style={{fontSize:15,color:"red"}}>{this.state.emailError}</div>
              <div className="mv3">
                <label className="db fw6 lh-copy f6" htmlFor="password">Password</label>
                <input
                  className="b pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="password"
                  name="password"
                  id="password"
                  onChange={this.onPasswordChange}
                />
              </div>
              <div style={{fontSize:15,color:'red'}}>{this.state.passwordError}</div>
            </fieldset>
            <div className="">
              <input
                onClick={this.onSubmitSignIn}
                className="b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib"
                type="submit"
                value="Sign in"
              />
            </div>
            <div className="lh-copy mt3">
              <p  onClick={() => onRouteChange('register')} className="f6 link dim black db pointer">Register</p>
            </div>
          </div>
        </main>
      </article>
    );
  }
}

export default Signin;
