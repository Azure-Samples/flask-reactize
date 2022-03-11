import * as React from 'react';

const userAddEndpoint = "/reqres/users";

const userAdd = async (user) => {

  return await fetch(userAddEndpoint, {
      method: "POST",
      headers:  {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(user)
    })
};

class UserAdd extends React.Component {
    
    constructor() {
        super();
        this.state = {
            userAdded: false,
            newUserID: null
        };
    }

    addUser = (e) => {
        e.preventDefault();
        
        const name = document.getElementById("name").value
        const job = document.getElementById("job").value

        // Call the API
        userAdd({
            "name": name,
            "job": job
        }).then(response => {
            if (response.ok) {
                response.json().then(json => {
                    this.setState(
                        {
                            userAdded: true,
                            newUserID: json.id
                        }
                    )
                })
            }
        })
    }

    render() {
        return (
            <div>
                <h2>Add a user</h2>
                <form onSubmit={this.addUser}>
                    <div class="form-field">
                        <label for="name">New user's name:</label>
                        <input type="text" id="name" />
                    </div>

                    <div class="form-field">
                        <label for="job">New user's job:</label>
                        <input type="Text" id="job" />
                    </div>

                    <button type="submit">Add user</button>
                </form>
                {
                    this.state.userAdded
                    ?
                    <span class="green">User added successfuly. New ID: {this.state.newUserID}</span>
                    :
                    <span></span>
                }
            </div>
        );
    }
}

export default UserAdd;