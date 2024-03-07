import streamlit as st
import yaml  # Make sure to have PyYAML installed
from yaml import SafeLoader
from authenticate import Authenticate  # Import your authentication module

_RELEASE = True
result = ""
if _RELEASE:
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

    # Check if the user is logged in
    #if not st.session_state.get("authentication_status"):
        # Creating a login widget
    try:
        authenticator.login()

    except Exception as e:
        st.error(e)

    if st.session_state["authentication_status"] is True:
        # Welcome message
        authenticator.logout()
        st.write(f'Welcome *{st.session_state["name"]}*')
        st.title('Home')
        
    elif st.session_state["authentication_status"] is False:
        st.error("error")
    elif st.session_state["authentication_status"] is None:
        st.warning('Please Enter Username/password')
        # Register button
        result = st.button('Register')
    if result:
        st.session_state["register_clicked"] = True

    if st.session_state.get("register_clicked", False):
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                preauthorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                config['credentials']['username'] = username_of_registered_user
                st.session_state["name"] = name_of_registered_user
                    # Save the new username to the config file
                st.session_state["authentication_status"] = True  # Set authentication status after successful registration
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)

        # Password reset widget



    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
