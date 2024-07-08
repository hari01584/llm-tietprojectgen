from contextlib import contextmanager
import uuid
from pydantic import BaseModel

class UserModel(BaseModel):
    user_name: str
    email: str
    password_hashed: str
    credits: int = 0
    pending_confirmations: list[str] = []
    transactions_id: list[str] = []
    project_name: str = ""
    company_name: str = ""
    is_verified: bool = False
    is_premium: bool = False
    verification_token: str = ""
    referral_code: str = ""
    referral_code_count: int = 0
    referral_code_used: str = ""
    is_admin: bool = False

# Setup database
import dictdatabase as DDB

# Get path of this directory where this file is located
import os
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
# Go one level up is root
ROOT_DIR = os.path.abspath(os.path.join(DIR_PATH, os.pardir))

DDB.config.storage_directory = os.path.join(ROOT_DIR, "ddb_storage")

def get_user_data(unique: str):
    user_data = DDB.at(f"users/{unique}").read()
    # Check if it is in form of UserModel
    if not user_data:
        return None
    return UserModel(**user_data)

def db_check_if_user_exists(unique: str):
    return DDB.at(f"users/{unique}").exists()

def verify_hashed_password(email: str, hashed_password: str) -> bool:
    if not db_check_if_user_exists(email):
        return False

    user_data = get_user_data(email)
    return user_data.password_hashed == hashed_password

def save_user_data(unique: str, user_data: UserModel):
    # Also create a referral code
    # if not user_data.referral_code:
    #     DDB.at(f"referral/{user_data.referral_code}").create(user_data.email, True)

    DDB.at(f"users/{unique}").create(user_data.model_dump(), True)

def set_verified(unique: str):
    user_data = get_user_data(unique)
    user_data.is_verified = True
    user_data.credits += 5
    save_user_data(unique, user_data)

def coins_delta(unique: str, delta: int):
    user_data = get_user_data(unique)
    user_data.credits += delta
    save_user_data(unique, user_data)

def redeem_referral_code(unique: str, referral_code: str) -> list[bool, str]:
    # Get current user
    user_data = get_user_data(unique)
    # Check if user exists
    if not user_data:
        return [False, "User does not exist!"]
    if user_data.referral_code == referral_code:
        return [False, "You cannot refer yourself!"]
    if user_data.is_verified == False:
        return [False, "You need to verify your email first!"]

    # Check if user has already redeemed a referral code
    if user_data.referral_code_used != "":
        return [False, "You have already redeemed a referral code!"]

    # Scan all users to find who has this referral code
    data = DDB.at("users/*", where=lambda x, y=referral_code: y["referral_code"] == referral_code).read()
    if not data:
        return [False, "Invalid referral code!"]
    
    # Get value of the first key
    referee_parent_email = list(data.keys())[0]
    referee_data = data[referee_parent_email]
    # Convert to UserModel
    referee = UserModel(**referee_data)
    
    # Mark the referral code as used
    user_data.referral_code_used = referral_code
    user_data.credits += 2

    # Update the referee's credits
    referee.credits += 3
    referee.referral_code_count += 1

    # Save the data
    save_user_data(unique, user_data)
    save_user_data(referee.email, referee)

    return [True, "Referral code redeemed successfully!"]

def save_user_feedback(feedback_data: dict):
    key = str(uuid.uuid4())
    DDB.at(f"feedback/{key}").create(feedback_data)

def save_usage_log(user: UserModel):
    # Get current time (that can be sorted properly)
    from datetime import datetime
    current_date = datetime.now()
    DDB.at(f"usage_log/{current_date.isoformat()}").create({
        "user_name": user.user_name,
        "email": user.email,
        "project_name": user.project_name,
        "company_name": user.company_name,
        "credits": user.credits,
        "timestamp": current_date.isoformat()
    })

def get_usage_log():
    all_data = DDB.at("usage_log/*").read()
    # Convert to list of dict
    all_data_list = []
    for key in all_data:
        all_data_list.append(all_data[key])
    return all_data_list

#     return user_data
if __name__ == "__main__":
    # Test
    print(redeem_referral_code("hari01584@gmail.com", "MNNQRS"))