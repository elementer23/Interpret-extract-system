import os
import subprocess
import time
import requests
from dotenv import load_dotenv

load_dotenv()

def connect_to_label_studio(email: str, pwd: str):
    env_var = os.environ.copy()
    env_var["LABEL_STUDIO_USERNAME"] = email
    env_var["LABEL_STUDIO_USERNAME"] = pwd
    env_var["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
    env_var["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"

    cmd = ["uvx", "--with", "label-studio", "--python", "3.12", "label-studio", "start", "--port", "8080"]
    print("starting Label Studio in isolated Python 3.12 environment!")
    process = subprocess.Popen(cmd, env=env_var)

    print("Waiting for the initialization of the interface...")
    time.sleep(5)

    LABEL_STUDIO_URL = os.getenv("LABEL_STUDIO_URL", "http://localhost:8080")
    LABEL_STUDIO_API_KEY = os.getenv("LABEL_STUDIO_API_KEY", "placeholder")

    headers = {
        "Authorization": f"Token {LABEL_STUDIO_API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(f"{LABEL_STUDIO_URL}/api/projects", headers=headers)
        if response.status_code == 200:
            projects = response.json().get("results", [])
            print(f"successfully connected! Amount of projects present: {len(projects)}")
        else:
            print(f"Servers is working, API-verification failed (Status: {response.status_code}).")
            print("Check if your 'API_KEY' is valid or has been properly set.")
    except requests.exceptions.ConnectionError:
        print("Couldn't connect. Server could still start or the port is already in use.")
    
    return process


