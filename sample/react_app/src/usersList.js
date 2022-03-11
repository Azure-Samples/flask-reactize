import * as React from 'react';

const usersListEndpoint = "/reqres/users";

const getUsers = async () => {

  return await fetch(usersListEndpoint, {
      method: "GET",
      headers:  {
          'Content-Type': 'application/json'
      }
    })
};

class UsersList extends React.Component {
    
    constructor() {
        super();
        this.state = {
            isFetching: true,
            users: [] 
        };
    }

    componentDidMount() {
        getUsers()
            .then((response) => {
                if (response.ok) {
                    response.json().then(json => {
                        this.setState(
                            {
                                isFetching: false,
                                users: json.data.map(x => x.last_name + " " + x.first_name)
                            }
                        )
                    })
                }
            })
            .catch(() => {
                this.setState({ isFetching: false });
            });
    }
    
    render() {
        return (
            <div>
                <h2>List of users</h2>
                <ul>
                    {
                        this.state.isFetching
                        ?
                            <i>Fetchin' data ...</i>
                        :
                            this.state.users.map((item, index) =>
                                <li key={index}>{item}</li>
                            )
                        }
                </ul>
            </div>
        );
    }
}

export default UsersList;