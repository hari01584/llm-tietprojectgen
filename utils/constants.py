from decouple import config

STREAMLIT_DOMAIN = 'https://tietprojgen.skullzbones.com'

SIGNUP_URL = f"{STREAMLIT_DOMAIN}/Sign_Up"
GENERATE_REPORT = f"{STREAMLIT_DOMAIN}/Generate_Report"
CREDITS_PAGE = f"{STREAMLIT_DOMAIN}/Credits"
USER_TABLE = 'users'

# TODO: switch our db over to mysql
DB_URL = f"postgresql://{config('DB_USER')}:{config('DB_PWD')}@{config('DB_HOST')}:{config('DB_PORT')}/{config('DB_NAME')}"