import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit.components.v1 as components

from hasher import Hasher
from authenticate import Authenticate

_RELEASE = True

while  _RELEASE:
    # Loading config file
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Creating the authenticator object
    authenticator = Authenticate(
        config['credentials'],
        config['cookie']['name'], 
        config['cookie']['key'], 
        config['cookie']['expiry_days'],
        config['preauthorized']
    )

    # Creating a login widget
    try:
        authenticator.login()
    except Exception as e:
        st.error(e)
        

    if st.session_state["authentication_status"] is False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
    elif st.session_state["authentication_status"]:
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Some content')


    # Creating a new user registration widget
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False)
        if email_of_registered_user:
            st.success('User registered successfully')
    except Exception as e:
        st.error(e)


    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
