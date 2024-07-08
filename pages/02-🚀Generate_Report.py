import json
import os
import tempfile
import streamlit as st
from utils.auth import login_st_form, get_current_logged_in_user
from utils.constants import CREDITS_PAGE
from streamlit.errors import StreamlitAPIException
from utils.model import UserModel, coins_delta, save_usage_log
from llm_executor.call_promptflow import execute_flow
from latex_executor.compile_latex import compile_latex

try:
    st.set_page_config(page_title='Generate', page_icon='🚀', initial_sidebar_state="auto", menu_items=None)
except StreamlitAPIException as e:
    pass

st.title('🚀 Generate Your Report!')

logged_in = login_st_form()

def nary_img_with_caption(key_prefix: str, n: int, title: str = "Upload Images") -> list[any, str]:
    image_boxes = []
    with st.expander(title):
        for i in range(n):
            # File uploader
            uploaded_file = st.file_uploader(f"Choose file {i+1}", key=f"{key_prefix}_file_uploader_{i}")
            # Text input for caption
            caption = st.text_input(f"Enter a caption for Image {i+1}", key=f"{key_prefix}_text_input_{i}")
            image_boxes.append((uploaded_file, caption))

    return image_boxes

def get_var_name(var):
    for name, value in globals().items():
        if value is var:
            return name

def report_generation_start(user_data: UserModel, required_fields_map: dict, not_required_fields_map: dict, transform_image_fields: dict, debug_mode: bool = False):
    if user_data.credits < 5:
        st.error(f"You do not have enough credits to generate a report, Please check [credits page]({CREDITS_PAGE}) to get more.")
        return
    
    resultant_file_bytes = None

    # Create temp directory for assets
    with tempfile.TemporaryDirectory() as assets_temp_dir:
        print(f"Temp Directory: {assets_temp_dir}")
        with st.status("Generating Report...") as status:
            # Required Fields
            for key, value in required_fields_map.items():
                if not value:
                    raise Exception(f"Please fill all required fields, {key.replace('_', ' ').title()} is required!")
                
            st.success("Validation Completed, All required fields are filled!")

            # Convert date to proper format
            if not_required_fields_map["project_date"]:
                not_required_fields_map["project_date"] = not_required_fields_map["project_date"].strftime("%B %Y")

            # Also convert keywords to list
            if required_fields_map["methodology_keywords"]:
                required_fields_map["methodology_keywords"] = [keyword.strip() for keyword in required_fields_map["methodology_keywords"].split(",")]

            # Save project completion letter to file
            if not_required_fields_map["project_completion_letter"]:
                project_completion_letter = not_required_fields_map["project_completion_letter"]
                extension = os.path.splitext(project_completion_letter.name)[1]
                save_path = os.path.join(assets_temp_dir, f"project_completion_letter{extension}")
                with open(save_path, mode='wb') as w:
                    w.write(project_completion_letter.read())
                not_required_fields_map["project_completion_letter"] = f"project_completion_letter{extension}"

            # Then transform image fields
            for key, value in transform_image_fields.items():
                if not value:
                    continue

                transformed_images = []
                for i, (image, caption) in enumerate(value):
                    # Save byteio array to file
                    if image:
                        # Get extension from image name
                        extension = os.path.splitext(image.name)[1]
                        filename = f"{key}_{i}{extension}"
                        save_path = os.path.join(assets_temp_dir, filename)
                        with open(save_path, mode='wb') as w:
                            w.write(image.read())

                        transformed_images.append((filename, caption))

                # Replace the original value with transformed images
                transform_image_fields[key] = transformed_images

            if debug_mode:
                # Dump transformed images
                st.info("Transformed Images: " + json.dumps(transform_image_fields, indent=2))

            # Use LLM to process/transform and generate more content :)
            llm_input_data = {**required_fields_map, **not_required_fields_map, **transform_image_fields}
            if debug_mode:
                st.info("LLM Input Data: " + json.dumps(llm_input_data, indent=2))

            output_data = execute_flow(**llm_input_data)
            if debug_mode:
                st.info(json.dumps(output_data, indent=2))

            st.success("Enrichment Done Successfully!")

            # Now finally compile the latex
            try:
                final_output_path = compile_latex(user_data.email, assets_temp_dir, {**required_fields_map, **not_required_fields_map, **transform_image_fields, **output_data})
                with open(final_output_path, "rb") as pdf_file:
                    resultant_file_bytes = pdf_file.read()

                st.success("Report Generation Completed Successfully! Please check your email for the report.")
            except Exception as e:
                st.error(f"Error while generating report: {e}, Check email for logs and raw files.")

            # Finally deduct credits
            coins_delta(user_data.email, -5)
            st.success("5 Credits Deducted!")

    st.success("Report Generation Completed Successfully!")
    if resultant_file_bytes:
        st.download_button(label="Download Report", data=resultant_file_bytes, file_name=f"report.pdf", mime='application/octet-stream', use_container_width=True)
    st.markdown("Please note, We DO NOT keep any cache/record of your data, It is deleted after the report is generated. Please make sure to download it now!")
    st.markdown("In case you missed it, A copy of report is also sent to your email.")
    save_usage_log(user_data)

if logged_in:
    user_data: UserModel = get_current_logged_in_user()
    st.info(f"Welcome {user_data.user_name}! You currently have {user_data.credits} credits, Each report cost 5 credits!")
    st.title('Generate Report')
    with st.form(key='generate_report'):
        st.subheader('User Information')
        student_name = st.text_input('Name (Used from Registration Only)', value=user_data.user_name, disabled=True)
        student_rollno = st.text_input('Rollno (eg. 102030xx)')

        st.subheader('Academic Information')
        department_name = st.selectbox('Department', ['Computer Science & Engineering Department', 'Electrical and Instrumentation Engineering Department', 'Electronics & Communication Engineering Department', 'Mechanical Engineering Department', 'Civil Engineering Department', 'Information Technology Department'])
        degree_name = st.selectbox('Full Degree Name', ['Bachelor of Engineering in Computer Engineering', 'B. Tech (Electrical Engineering)', 'Bachelor of Engineering in Electronics & Computer Engineering', 'Bachelor of Engineering in Mechanical Engineering', 'Bachelor of Engineering in Civil Engineering', 'Bachelor of Engineering in Information Technology'])
        # Add small text telling users to mail/contact for other degree names
        st.markdown("If your department/degree name is not listed, please report at [this email](mailto:tietprojectreport@skullzbones.com)")

        st.subheader('Project Information')
        project_title = st.text_input('Project Title (Used from Registration Only)', value=user_data.project_name, disabled=True)
        project_date = st.date_input('Project Date', value="today")
        industry_mentor_name = st.text_input('Industry Mentor Name')
        faculty_mentor_name = st.text_input('Faculty Mentor Name')
        project_completion_letter = st.file_uploader('Project Completion Letter (Image Only)', type=['png', 'jpg', 'jpeg'])

        st.subheader('Report Information')
        company_name = st.text_input('Company Name (Used from Registration Only)', value=user_data.company_name, disabled=True)
        company_profile = st.text_area('Company Profile')
        st.markdown("""
        - Mention your company name
        - Your role, how it aligns with this company (very shortly)
        - eg. 'I worked as a Software Developer Intern at Skullz & Bones, where I developed a web application for their clients.'
        - or  'I work in Heathcliff which is a progressive US Bank. I am a backend developer there, working over transaction searches of various merchants of Heathcliff.'
        - NOTE: If your company is newly registred or not well known, please provide a brief description of the company manually.
        """)

        introduction_input = st.text_area('Introduction')
        st.markdown("""
        - What is this project about?
        - What do you want to achieve with this project?
        - How will this project help with problem? (Briefly)
        - Tell background of the project/the need of the project.
        - eg. 'Skullzbones is a startup that provides services to the students of Thapar Institute of Engineering & Technology. They create applications which help users to get their projects done, This is very essential for lazy students/working students .'
        - or  'As a leading bank in the US, Heathcliff has a lot of transactions happening every day. They need a system to search for transactions of various merchants of Heathcliff, With my work I hope to optimize the search process.'
        """)
        introduction_input_images = nary_img_with_caption("introduction_images", 3, title="Upload Supporting Images for Introduction (like screenshots, diagrams, etc.)")


        background_input = st.text_area('Background')
        st.markdown("""
        - Background of the problem
        - Your motivation, alignment if any
        - Basically setup the stage for the project
        - eg. 'Automation still seemingly easy is not, it requires a lot of effort and time. There are many tools available for automation but they are not user friendly, they require a lot of technical knowledge to operate. This is where Skullz & Bones comes in, they provide a user friendly interface for automation. I liked their cause because as someone who programs, I know how hard it is to automate things, and I want to make it easier for others.'
        - or  'Transactions occour in a bank every second, and it is very hard to search for a particular transaction. Heathcliff has a lot of transactions happening every day. They need a system to search for transactions of various merchants of Heathcliff, With my work I hope to optimize the search process.'
        """)
        background_images = nary_img_with_caption("background_images", 3, title="Upload Supporting Images for Background (like screenshots, diagrams, etc.)")

        objectives_input = st.text_area('Objectives')
        st.markdown("""
        - What are the objectives of the project?
        - What tasks will you complete to mark project success?
        - Can also include (recommended) learning and developments, (ie learn react routers, etc) and interpersonal skills (ie work with team, manage time, etc.)
        - Please also mention specific techstacks, tools, etc. if any. Don't make them vague but rather give milestones based on them.
        - IMPORTANT: These objectives will be used to evaluate your performance, Careful what you write!
        - eg. 'Creating logic to automate report generation, it includes writing frontend code to let user interact with tool (in Streamlit), An LLM framework that can generate content based on user input, and a backend that can handle all the requests.'
        - or  'Using reactjs to create transaction dashboard, adding widgets for search, filter, etc. Using Django to create backend that can handle requests from frontend, and can interact with database.'
        """)

        methodology_input = st.text_area('Methodology')
        methodology_keywords = st.text_input('Top Keywords (Comma Separated)', help="eg. Agile, FastAPI, Promptflow, git etc.")
        st.markdown("""
        - Include software development lifecycle, tools, technologies, frameworks, etc, including meeting schedules, etc.
        - Include project planning, requirements gathering, design, etc.
        - Include project management tools, version control, etc. (eg. Jira, Git, etc.)
        - Include testing, deployment, etc. (eg. Unit Testing using Pytest, Deployment using Heroku, etc.)
        - Include programming languages, libraries, etc. (eg. Python, ReactJS, etc.) (eg. ReactJS frontend using Redux, Chakra UI, etc.)
        - NOTE: This section is the beef and bones of your project, make sure to include everything you did in this project.
        - NOTE: To make you write less, You can just breifly mention your tools you used, and then add the same into list of keywords (We will automatically add their description for you!)
        - NOTE: Strongly recommended to include relevant image with caption to support your methodology.
        - eg. 'We followed Agile methodology, used FastAPI for backend, ReactJS for frontend, Git for version control, and Docker for containerization. The project was divided into 3 sprints, each sprint was 2 weeks long. We used Jira for project management, and Pytest for unit testing.'
        - top keywords: Agile, FastAPI, Promptflow, git, docker
        """)

        methodology_images = nary_img_with_caption("methodology_images", 3, title="Upload Supporting Images for Methodology (like screenshots, diagrams, etc.)")

        observation_findings_input = st.text_area('Observation & Findings')
        st.markdown("""
        - What are the key takeaways from the project? Mention how working on this project helped you grow as a professional.
        - Are there any tools, technologies, frameworks, etc. that you found useful or not useful? Mention them here.
        - Can also mention about the impact of working in team, managing time, etc. Or how methodologies helped you in the project.
        - eg. 'Working in scrumm, I learned the tredemous impacts of daily standups, sprint planning, and retrospectives. I also learned how to work with a team, and how to manage time effectively. I also learned how to use FastAPI, and ReactJS, which are very useful tools.'
        - or  'While creating dashboard with fastapi, I learned how to create APIs, and how to handle requests. I learned the hard skills whose I used to dread, and now I am confident in them.'
        - or 'I observed the slow nature of getting products/ideas approved in a big company like Heathcliff. Aside from learning and all, I also learned how to get my ideas approved, and how to work with a big team.'
        """)

        limitations_input = st.text_area('Limitations')
        st.markdown("""
        - What are the limitations of the project?
        - What could have been done better?
        - What are the constraints that you faced?
        - eg. 'We had a tight deadline, and we could not implement all the features that we wanted to. We also faced issues with the deployment, as the server was not responding properly.'
        - or  'Depedency on permits and regulations of bank, Improper communication and disarray in team, Not planning properly before starting the project.'
        """)

        conclusions_future_work_input = st.text_area('Conclusions & Future Work')
        st.markdown("""
        - What are the conclusions of the project? What did you achieve? Helpful to mention metrics/impact if any.
        - If you were to work on this project again, what would you do differently?
        - What are the future plans for this project?
        - eg. 'We successfully created a dashboard that can search for transactions of various merchants of Heathcliff. We also implemented a feature to filter transactions based on date, amount, etc. We also deployed the project on Heroku. In future, we plan to add more features like email notifications, etc.'
        - or  'Could have planned architecture better, and used tools like NextJs instead of ReactJs. In future, I plan to add more features like user authentication, etc.'
        """)

        debug_mode = st.checkbox('Debug Mode', value=True)
        generate_report = st.form_submit_button('Generate Report', use_container_width=True)

    if generate_report:
        required_fields_map = {
            "student_name": student_name,
            "student_rollno": student_rollno,
            "project_title": project_title,
            "industry_mentor_name": industry_mentor_name,
            "faculty_mentor_name": faculty_mentor_name,
            "company_name": company_name,
            "company_profile": company_profile,
            "introduction_input": introduction_input,
            "background_input": background_input,
            "objectives_input": objectives_input,
            "methodology_input": methodology_input,
            "methodology_keywords": methodology_keywords,
            "observation_findings_input": observation_findings_input,
            "limitations_input": limitations_input,
            "conclusions_future_work_input": conclusions_future_work_input,
        }

        not_required_fields_map = {
            "project_completion_letter": project_completion_letter,
            "department_name": department_name,
            "degree_name": degree_name,
            "project_date": project_date,
        }

        transform_image_fields = {
            "introduction_images": introduction_input_images,
            "background_images": background_images,
            "methodology_images": methodology_images,
        }

        report_generation_start(user_data, required_fields_map, not_required_fields_map, transform_image_fields, debug_mode)