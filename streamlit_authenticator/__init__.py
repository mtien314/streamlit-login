import streamlit as st
import yaml  # Make sure to have PyYAML installed
from yaml import SafeLoader
from authenticate import Authenticate  # Import your authentication module

_RELEASE = True

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
    if not st.session_state.get("authentication_status"):
        # Creating a login widget
        try:
            authenticator.login()
            st.session_state["authentication_status"] = True
            st.session_state["username"] = config['credentials']['username']  # Assuming username is stored in credentials
        except Exception as e:
            st.error(e)

    if st.session_state.get("authentication_status"):
        # Welcome message
        st.write(f'Welcome *{st.session_state["username"]}*')
        st.title('Home')
    
        # Register button
        if st.button('Register'):
            st.session_state["register_clicked"] = True

        if st.session_state.get("register_clicked", False):
            try:
                email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(
                    preauthorization=False)
                if email_of_registered_user:
                    st.success('User registered successfully')
                    config['credentials']['username'] = username_of_registered_user
                    # Save the new username to the config file
                    with open('config.yaml', 'w') as file:
                        yaml.dump(config, file, default_flow_style=False)
            except Exception as e:
                st.error(e)

        # Password reset widget
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

        # Update user details widget
        try:
            if authenticator.update_user_details(st.session_state["username"]):
                st.success('Entries updated successfully')
        except Exception as e:
            st.error(e)

    else:
        st.error('Username/password is incorrect' if st.session_state["authentication_status"] is False else 'Please Enter Username/password')

    if 'controllo' not in st.session_state or st.session_state['controllo'] == False:
        captcha_control()

    # Saving config file
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
