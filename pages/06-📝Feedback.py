import streamlit as st
from utils.auth import login_st_form, get_current_logged_in_user
from streamlit.errors import StreamlitAPIException
from utils.model import UserModel, save_user_feedback, set_verified
from utils.func import send_user_feedback_email

try:
    st.set_page_config(page_title='Feedback', page_icon='📝', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

def form_submit(all_data_dict: dict):
    if not all_data_dict["name"]:
        st.error("Please enter your name.")
        return
    if not all_data_dict["feedback"]:
        st.error("Please enter your feedback.")
        return
    
    # Save feedback to database
    save_user_feedback(all_data_dict)
    send_user_feedback_email(all_data_dict)
    
    st.success("Feedback submitted successfully!")

st.title('📝 Feedback form')
with st.form(key="feedback_form"):
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email (In case for reply):")
    feedback = st.text_area("Enter your feedback (Please be truthful):")
    st.markdown("Below fields are optional (but recommended to fill)")

    with st.expander("User Satisfaction Slider"):
        inputs_complexity = st.slider("How complex were filling texts in report generation?", 1, 5, 3)
        inputs_clarity = st.slider("How clear were the instructions?", 1, 5, 3)
        generated_content = st.slider("How satisfied were you with the generated content? (Without formatting)", 1, 5, 3)
        formatted_content = st.slider("How satisfied are you with document formatting/structure?", 1, 5, 3)
        overall_satisfaction = st.slider("Overall satisfaction with the tool?", 1, 5, 3)
        ui_ux = st.slider("How satisfied are you with the UI/UX?", 1, 5, 3)
        how_like_recommend = st.slider("How likely are you to recommend this tool to others?", 1, 5, 3)

    with st.expander("Would you like to be contacted for further feedback?"):
        contact = st.checkbox("Yes, I would like to be contacted for further feedback.")

    submit = st.form_submit_button("Submit", use_container_width=True)

if submit:
    all_data_dict = {
        "name": name,
        "email": email,
        "feedback": feedback,
        "inputs_complexity": inputs_complexity,
        "inputs_clarity": inputs_clarity,
        "generated_content": generated_content,
        "formatted_content": formatted_content,
        "overall_satisfaction": overall_satisfaction,
        "ui_ux": ui_ux,
        "how_like_recommend": how_like_recommend,
        "contact": contact
    }

    form_submit(all_data_dict)  