# Write a function, that simply compiles latex file to pdf

from datetime import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import traceback
import json

# Get path of this directory where this file is located
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# Go one directory up to get to the root directory
ROOT_DIR = os.path.abspath(os.path.join(DIR_PATH, os.pardir))
# Add the path to the sys path
sys.path.append(ROOT_DIR)
from utils.func import send_project_generation_report

# The path to promptflow files are one directory below, go
PATH_TEMPLATE_DIR = os.path.join(ROOT_DIR, "latex_tiet_format")

QUICK_LLM_REPLACEMENTS = {
    "@STUDENTNAME@": "student_name",
    "@PROJECTNAME@": "project_title",
    "@PROJECTDATE@": "project_date",
    "@ROLLNO@": "student_rollno",
    "@INDUSTRIALMENTORNAME@": "industry_mentor_name",
    "@FACULTYMENTORNAME@": "faculty_mentor_name",
    "@DEPARTMENTNAME@": "department_name",
    "@DEGREEFULLNAME@": "degree_name",
    "@COMPANYNAME@": "company_name",
    "@ABSTRACTGENERATED@": "abstract_generated",
    "@CERTIFICATECOMPLETIONIMGNAME@": "project_completion_letter",
    "@COMPANYPROFILEGENERATED@": "company_profile_generated",
    "@INTRODUCTIONGENERATED@": "introduction_generated",
    "@BACKGROUNDGENERATED@": "background_generated",
    "@OBJECTIVESGENERATED@": "objectives_generated",
    "@METHODOLOGYGENERATED@": "methodology_generated",
    "@OBSERVATIONSFINDINGSGENERATED@": "observations_generated",
    "@LIMITATIONSGENERATED@": "limitations_generated",
    "@CONCLUSIONSGENERATED@": "conclusions_generated",
}

def write_log(temp_dir, message, filename='replace_logs.txt'):
    # Open the file in append mode
    with open(os.path.join(temp_dir, filename), 'a') as file:
        # Get the current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Format the log message
        log_message = f"{current_time} - {message}\n"
        # Write the log message to the file
        file.write(log_message)

def process_latex_files(temp_dir: str, context_data: dict):
    # Create temp log file inside the temp_dir
    # with open(os.path.join(temp_dir, "replace_logs.txt"), "w") as f:
    #     f.write("REPLACEMENT LOGS\n")
    replace_files_paths = [
        "main.tex",
    ]

    tokens_that_couldnt_be_replaced = []

    write_log(temp_dir, "Starting replacement of data in latex files")

    for file_path in replace_files_paths:
        # Read whole file
        with open(os.path.join(temp_dir, file_path), "r") as f:
            file_data = f.read()

            # Remove sections of code if not avaliable,
            if "project_completion_letter" not in context_data or context_data["project_completion_letter"] == "" or not context_data["project_completion_letter"]:
                start_token = "%REMOVEIFNOCOMPLETIONSTART%"
                end_token = "%REMOVEIFNOCOMPLETIONEND%"
                # Remove all the data between the start and end tokens
                file_data = file_data.replace(file_data[file_data.find(start_token):file_data.find(end_token) + len(end_token)], "")

            # Use quick llm replacements to replace the data
            for key, value in QUICK_LLM_REPLACEMENTS.items():
                if key in file_data:
                    if value in context_data:
                        file_data = file_data.replace(key, context_data[value])
                    else:
                        write_log(temp_dir, f"[CRITICAL] Cannot replace {key} with {value}, As not found in context data")
                        tokens_that_couldnt_be_replaced.append(key)
                else:
                    write_log(temp_dir, f"Skipping token {key}, As not found in {file_path}")

        # Write the data back to the file
        with open(os.path.join(temp_dir, file_path), "w") as f:
            f.write(file_data)

    # Also write bibliography file
    if "bibliography" in context_data:
        with open(os.path.join(temp_dir, "includes", "ref.bib"), "w") as f:
            f.write(context_data["bibliography"])

def pack_and_get_path(email: str, temp_dir: str):
    # If there already exists a zip file, delete it
    if os.path.exists(os.path.join(temp_dir, f"{email}_latex_compile_logs.zip")):
        os.remove(os.path.join(temp_dir, f"{email}_latex_compile_logs.zip"))

    # Create temporary dir
    with tempfile.TemporaryDirectory() as zip_temp_dir:
        path = shutil.make_archive(os.path.join(zip_temp_dir, f"{email}_latex_compile_logs"), 'zip', temp_dir)
        # Copy the zip file to the temporary directory
        shutil.copy(path, temp_dir)

    final_path = os.path.join(temp_dir, f"{email}_latex_compile_logs.zip")
    print("ZIP FILE GENERATED", final_path)
    return final_path


def run_command(command: list[str], temp_dir: str, label: str):
    with open(os.path.join(temp_dir, "compile_logs.txt"), 'a') as logfile:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        logfile.write(f"{label}\n\n")
        while True:
            line = proc.stdout.readline()
            if line == '' and proc.poll() is not None:
                break
            if line:
                sys.stdout.write(line)
                logfile.write(line)
                logfile.flush()  # Ensure the log is written immediately
        proc.wait()

def compile_latex(email: str, assets_temp_dir: str, context_data: dict):
    # Dump the context data to a file
    # with open("/home/hsk/Desktop/Startups/tietprojrepo.ai/tietprojstream/testing/context_data.json", "w") as f:
    #     f.write(json.dumps(context_data))
    # with open("/home/hsk/Desktop/Startups/tietprojrepo.ai/tietprojstream/testing/assets_temp_dir.txt", "w") as f:
    #     f.write(str(assets_temp_dir))

    # Get current directory (make backup)
    current_dir = os.getcwd()

    # First create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # Copy the file to the temporary directory
            # shutil.copytree(PATH_TEMPLATE_DIR, temp_dir)
            # Shutil copy all files from the template directory to the temporary directory while maintaining the directory structure
            destination = shutil.copytree(PATH_TEMPLATE_DIR, temp_dir, dirs_exist_ok=True)
            print("COPIED FILES TO TEMP DIR", destination)

            # Also copy the assets_temp_dir to the temporary directory
            shutil.copytree(assets_temp_dir, os.path.join(temp_dir), dirs_exist_ok=True)

            process_latex_files(temp_dir, context_data)

            # Change directory to the temporary directory
            os.chdir(temp_dir)
            # Delete any main.pdf generated
            if os.path.exists("main.pdf"):
                os.remove("main.pdf")

            print("STARTING PDF GENERATION")
            # Compile the latex file to pdf

            run_command(["pdflatex", "-interaction=nonstopmode", "main.tex"], temp_dir, f"PDF GENERATION 0")
            # Then do bibliography
            run_command(["bibtex", "main"], temp_dir, f"BIBLIOGRAPHY GENERATION")
            run_command(["pdflatex", "-interaction=nonstopmode", "main.tex"], temp_dir, f"Final Typesetting")
            run_command(["pdflatex", "-interaction=nonstopmode", "main.tex"], temp_dir, f"Final BUILD CITE")

            print("PDF GENERATION COMPLETED")

            # Check if main.pdf is generated
            if os.path.exists("main.pdf"):
                print("PDF generated successfully")
            else:
                raise Exception("PDF generation failed..")

            # If successful, place this file to the assets_temp_dir
            shutil.copy("main.pdf", os.path.join(assets_temp_dir, f"{email}_main.pdf"))

            # Yay! PDF generated successfully, You can send it :)
            # First get path to the generated pdf
            pdf_path = os.path.join(temp_dir, "main.pdf")
            zip_path = pack_and_get_path(email, temp_dir)
            # Rather than sending, for now just print the path
            if email == "":
                # If email is empty, ie running in debug mode, so open file
                import webbrowser
                webbrowser.open_new(pdf_path)
            else:
                send_project_generation_report(email, [pdf_path, zip_path])
    
            print("SENT PDF TO USER")
            print("TEMP DIR IS", temp_dir)

            return os.path.join(assets_temp_dir, f"{email}_main.pdf")

        except Exception as e:
            # Pack whole directory and send it to the user
            zip_path = pack_and_get_path(email, temp_dir)
            print(zip_path)
            # TODO: ENABLE MAIL SEND
            send_project_generation_report(email, [zip_path], status="failed", extra_message=traceback.format_exc())
            print("SENT LOGS TO USER")
            raise e
        finally:
            # Set the directory back to the original directory
            os.chdir(current_dir)

if __name__ == "__main__":
    # with tempfile.TemporaryDirectory() as assets_temp_dir:
    #     final_res = compile_latex("hari01584@gmail.com", assets_temp_dir, {})
    temp_dump_path = ""
    dump_context_data = {}
    with open("/home/hsk/Desktop/Startups/tietprojrepo.ai/tietprojstream/testing/assets_temp_dir.txt", "r") as f:
        temp_dump_path = f.read()
    with open("/home/hsk/Desktop/Startups/tietprojrepo.ai/tietprojstream/testing/context_data.json", "r") as f:
        context_data = json.loads(f.read())

    compile_latex("", temp_dump_path, context_data)