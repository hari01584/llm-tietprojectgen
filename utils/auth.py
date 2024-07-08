import time
import uuid
import streamlit as st
from utils.constants import (
    STREAMLIT_DOMAIN,
    GENERATE_REPORT,
    SIGNUP_URL,
)
import jwt
from decouple import config
# from utils.stripe import get_create_checkout_session_url
import bcrypt
import pandas as pd
import extra_streamlit_components as stx
from utils.validator import Validator
from datetime import datetime, timedelta
# from sqlalchemy import create_engine
from utils.constants import DB_URL
import coloredlogs, logging
from .model import *
from .func import generateCapitalReferralCode, generateVerificationCode, send_verification_email

logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL'), logger=logger)
# psql_engine = create_engine(DB_URL)

@st.cache_resource(experimental_allow_widgets=True)
def get_manager():
    return stx.CookieManager(key='stream_cookie_key')

cookie_manager = get_manager()

# --------------------helpers
# -- encryption
def hash_password(password):
    # Generate a salt and hash the password with the salt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(input_password, hashed_password):
    # Check if the input password matches the hashed password
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

def get_current_logged_in_user() -> UserModel:
    return get_user_data(unique=st.session_state['email'])
# --users
class Authenticator():
    def __init__(self) -> None:
        self.validator = Validator()
        cookie_manager = stx.CookieManager()
        self.cookie_name = 'stream_cookie'
        self.key = 'stream_cookie_key'
        self.cookie_expiry_days = 7

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
            # TODO: add logout functionality
            # TODO: add reset / forgot password functionality
            # TODO: add google auth functionality
    
    def check_if_user_exists(self, email):
        return db_check_if_user_exists(unique=email)
    
    def register_user(self, username, email, password, project_name, company_name):
        is_valid_email = self.validator.validate_email(email=email)
        if not is_valid_email:
            raise Exception('Not a valid email')
        hashed_password = hash_password(password)
        user_exists = self.check_if_user_exists(email=email)
        if user_exists:
            raise Exception('User already exists')
        else:
            verification_code = generateVerificationCode()
    
            save_user_data(
                unique=email,
                user_data=UserModel(
                    user_name=username,
                    email=email,
                    credits=5, # New user gets 5 credits
                    password_hashed=hashed_password,
                    project_name=project_name,
                    company_name=company_name,
                    verification_token=verification_code,
                    referral_code=generateCapitalReferralCode()
                )
            )

            send_verification_email(email, verification_code, STREAMLIT_DOMAIN)

            return email
    
    def check_if_authenticated(self):
        logger.debug(f'st.session_state: {st.session_state}')
        if st.session_state['authentication_status']:
            # And check if email exist in our user
            if st.session_state['email'] and self.check_if_user_exists(st.session_state['email']):
                return True
        else:
            self._check_cookie()
            logger.debug(f'st.session_state: {st.session_state}')
            if st.session_state['authentication_status']:
                if st.session_state['email'] and self.check_if_user_exists(st.session_state['email']):
                    return True
        
        return False

    def check_user_login(self, email, password):
        # Check if the user exists
        if not self.check_if_user_exists(email):
            return False
        
        user_model = get_user_data(unique=email)
        hashed_pwd = user_model.password_hashed

        correct_password = verify_password(input_password=password, hashed_password=str.encode(hashed_pwd))
        if correct_password:
            st.session_state['email'] = email
            st.session_state['authentication_status'] = True
            self.exp_date = self._set_exp_date()
            self.token = self._token_encode()
            time.sleep(0.1)
            cookie_manager.set(self.cookie_name, self.token)
            time.sleep(0.1)
            cookie_manager.get_all(key="flush_key_cache")
            time.sleep(0.1)
            return True

        return False

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        return jwt.encode({
            # 'name':st.session_state['name'],
            'email':st.session_state['email'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> str:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        str
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        cookie_manager.get_all()
        time.sleep(0.1)
        # grabbed from here: https://github.com/mkhorasani/Streamlit-Authenticator/blob/main/streamlit_authenticator/authenticate.py
        self.token = cookie_manager.get(self.cookie_name)
        logger.debug(f'self.token: {self.token}')
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'email' in self.token:
                            st.session_state['email'] = self.token['email']
                            st.session_state['authentication_status'] = True


# ------------streamlit forms

def create_account_st_form():
    st.subheader('Create Account')
    st.caption(f"Already have an account? [Log in here]({GENERATE_REPORT})")
    authenticator = Authenticator()

    with st.form(key='registration_form'):
        email = st.text_input('Email')
        username = st.text_input('Your Name')
        password = st.text_input('Password', type='password')
        project_name = st.text_input('Project Name')
        company_name = st.text_input('Company Name')
        st.write("Please fill in the project and company name properly, as this will be used later for generating your reports (and cannot be changed without asking the Admin).")

        # Form submission button
        submit_button = st.form_submit_button(label='Sign Up', use_container_width=True)

    if submit_button:
        if email and username and password and project_name and company_name:
            # TODO: we need better logic here to ensure the account isn't being created before the
            # user is actually ready (otherwise we're getting "that account already exists" issues)
            try:
                user_id = authenticator.register_user(username=username, email=email, password=password, project_name=project_name, company_name=company_name)
            except Exception as e:
                st.error(f"Error: {e}")
                return None
            # checkout_session_url = get_create_checkout_session_url(email, stripe_customer)
            # st.link_button('Sign Up', url=checkout_session_url, type='primary')
            st.success('Account created successfully! Please log in to continue.')

            return user_id
        else:
            st.warning('Please enter your information above 👆🏻')


def login_st_form() -> bool:
    authentication_status = None
    authenticator = Authenticator()
    authenticated = authenticator.check_if_authenticated()
    logger.debug(f'st.session_state: {st.session_state}') 
    if authenticated:
        return True
    else:  
        placeholder = st.empty()
        with placeholder.form('Login', clear_on_submit=True):
            st.subheader('Login 🔒')
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            submit = st.form_submit_button('Submit')
            if submit:
                authentication_status = authenticator.check_user_login(email=email, password=password)
                st.session_state['authentication_status'] = authentication_status
                logger.debug(f'st.session_state: {st.session_state}')
        if authentication_status:
            placeholder.empty()
            return True
        elif authentication_status == False:
            st.error(f"Email/password is incorrect. Don't have an account yet? Create one here: [Sign Up](/Sign_Up)")
            return False
        elif authentication_status is None:
            st.warning(f"Don't have an account yet? Create one here: [Sign Up]({SIGNUP_URL})")
            return False