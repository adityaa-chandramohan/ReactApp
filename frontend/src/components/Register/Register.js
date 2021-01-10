import React from 'react';

const initialState = {
  email: '',
  password: '',
  name: '',
  nameError: '',
  emailError: '',
  passwordError: ''
}

const errorState = {
  nameError: '',
  emailError: '',
  passwordError: ''
}

class Register extends React.Component {
  constructor(props) {
    super(props);
    this.state = initialState
  }

  onNameChange = (event) => {
    this.setState({name: event.target.value})
  }

  onEmailChange = (event) => {
    this.setState({email: event.target.value})
  }

  onPasswordChange = (event) => {
    this.setState({password: event.target.value})
  }

  validate = () => {
   let emailError = "";
   let passwordError = "";
   let nameError = "";

   let passwordlength = this.state.password.length;

   if(!this.state.name){
     nameError = "name field cannot be blank.";
   }

   if(!this.state.email.includes("@") ){
     emailError = "invalid email";
   }

   if(!this.state.password){
     passwordError = "password field cannot be blank.";
   }

   if(passwordlength <= 8 || passwordlength >= 32){
     passwordError = "Password length must be between 8 and 32.";
   }

   if(emailError || passwordError || nameError)
   {
     this.setState({emailError,passwordError,nameError})
     return false;
   }

   return true;
 };

  onSubmitSignIn = () => {
    const isValid = this.validate()

    if(isValid){
    fetch('http://localhost:5000/api/register', {
      method: 'post',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        email: this.state.email,
        password: this.state.password,
        name: this.state.name
      })
    })
      .then(response => response.json())
      .then(user => {
        if (user) {
          this.props.loadUser(user)
          this.props.onRouteChange('home');
        }
      })
      .catch((error) => {
      this.setState({ passwordError: "Error in Registering user."})
      })

      this.setState(errorState)
    }
  }

  render() {
    return (
      <article className="br3 ba b--black-10 mv4 w-100 w-50-m w-25-l mw6 shadow-5 center">
        <main className="pa4 black-80">
          <div className="measure">
            <fieldset id="sign_up" className="ba b--transparent ph0 mh0">
              <legend className="f1 fw6 ph0 mh0">Register</legend>
              <div className="mt3">
                <label className="db fw6 lh-copy f6" htmlFor="name">Name</label>
                <input
                  className="pa2 input-reset ba bg-transparent hover-bg-black hover-white w-100"
                  type="text"
                  name="name"
                  id="name"
                  onChange={this.onNameChange}
                />
              </div>
              <div style={{fontSize:15,color:"red"}}>{this.state.nameError}</div>
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
              <div style={{fontSize:15,color:"red"}}>{this.state.passwordError}</div>
            </fieldset>
            <div className="">
              <input
                onClick={this.onSubmitSignIn}
                className="b ph3 pv2 input-reset ba b--black bg-transparent grow pointer f6 dib"
                type="submit"
                value="Register"
              />
            </div>
          </div>
        </main>
      </article>
    );
  }
}

export default Register;
