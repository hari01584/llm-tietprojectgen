import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit.errors import StreamlitAPIException

try:
    st.set_page_config(page_title='Introduction', page_icon='⭐', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

st.title('Introduction ⭐')
# Set page name shown in sidebar
# st.page

st.markdown(    
    """
### Welcome to Tiet Project Report Generator App!
Please read the following information carefully before proceeding:

### What does this app do?
- Automatically generate project reports for your last semester project.
- No need to worry about formatting, just provide the data and we will generate a beautiful report for you!
- No need to worry about the structure of the report, we will take care of that for you!
- No need to worry about the content, we will enrich your data and make it more structured!
- No need to worry about life, we will take care of that for you! (Just kidding, we can't do that)

Not a half-baked solution, where you have to generate texts in chunks and then copy-paste them in a word document, we generate a full report for you!

### How does it work?
This app works in 3 steps:
- **User Input**: Here you will provide lots of inputs about your project (in very simple language)
- **LLM Enrichment**: We use LLMs and a very complex pipeline to add more data and properly structure your report
- **Latex Generation**: We use Latex to generate a beautiful PDF report for you :)

## How to use this app?
- Go to Credits page to know more about your account balance, each report generation takes 5 credits..
- To earn credits, verify your email (get 5 credits), refer a friend (get 3 credits) or just straight up buy them!
- **New Launch Offer**: Get 5 credits for free on sign up! (Limited time offer)
- Go to Report Generation page and fill all required fields (while adding images, make sure to provide image name and description)
- Click on Generate Report and wait for your report to be generated!
- You will get an email with a download link to your report, you can also download it from the app itself!

Report any issues to the developer at [email](mailto:tietprojectreport@skullzbones.com)

## Data Security
- Any data you provide while generating reports are mailed to you and then completely deleted from our systems.
- Passwords are hashed and stored securely, even the developer cannot see your password.
- Usage logs only contain your name, email and timestamp of usage, no other data is stored.

## FAQ
- **What if I don't have enough credits?** - You can buy credits, refer a friend or verify your email to earn credits!
- **Why do I have to fill roll number, mentor names and other detailed instructions?** - Because we create full report, so anything required in the report should be provided by you.
- **Can I add images to the report?** - Yes, you can add images and provide a description for them.
- **How do I edit the generated report?** - We mail you raw LaTeX files along with the PDF. You can edit the LaTeX files and generate a new PDF, Use [Overleaf](https://www.overleaf.com/) to edit LaTeX files.

## Word of Warning (aka I am not Responsible)
There could be ethical concerns while using such a tool, make sure to review the generated report before submitting it to your college. 

**The developer is not responsible for any consequences of using this tool**

Additionally I strongly recommend to not use this tool for any kind of academic dishonesty, this tool is meant to help you generate reports faster, not to cheat in your academics! Users are adviced to double/triple check generated reports, and make sure the generated ones are good before blindly submitting them to your college.

Developed by [Harishankar Kumar](https://github.com/hari01584), Connect with me on [LinkedIn](https://www.linkedin.com/in/hsk4link/)
""")


sign_up = st.button('Start Now!', use_container_width=True)
if sign_up:
    switch_page('sign up')