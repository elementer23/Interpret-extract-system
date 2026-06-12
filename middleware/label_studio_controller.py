import os
import subprocess
import time
import requests
from typing import Any
from dotenv import load_dotenv
import psutil

load_dotenv()

LABEL_STUDIO_URL = os.getenv("LABEL_STUDIO_URL", "http://localhost:8080")
LABEL_STUDIO_API_KEY = os.getenv("LABEL_STUDIO_API_KEY", "placeholder")

class LabelStudioController():
    def __init__(self):
        self.running_process = None
        self.headers = {"Authorization": f"Token {LABEL_STUDIO_API_KEY}",
                        "Content-Type": "application/json"
                       }
        self.check_login = False

    def label_studio_login(self, email: str, pwd: str):
        env_var = os.environ.copy()
        env_var["LABEL_STUDIO_USERNAME"] = email
        env_var["LABEL_STUDIO_PASSWORD"] = pwd
        env_var["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
        env_var["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"

        cmd = ["uvx", "--with", "label-studio", "--python", "3.12", "label-studio", "start", "--port", "8080"]
        print("starting Label Studio in isolated Python 3.12 environment!")
        try:
            self.running_process = subprocess.Popen(cmd, env=env_var)

            print("Waiting for the initialization of the interface...")
            time.sleep(5)
        except Exception as e:
            print(f"Something went wrong while trying to start label studio: {e}")
            self.running_process = None

        if not LABEL_STUDIO_API_KEY == "placeholder":
            self.check_login = True 
        else:
            self.check_login = False
            return "You are logged in, but still haven't set your api key yet. Api privileges are restricted."


    def label_studio_projects(self):
        if not self.check_login: return None

        projects = None
        try:
            response = requests.get(f"{LABEL_STUDIO_URL}/api/projects", headers=self.headers)
            if response.status_code == 200:
                projects = response.json().get("results", [])
                print(f"successfully connected! Amount of projects present: {len(projects)}")
            else:
                print(f"Servers is working, API-verification failed (Status: {response.status_code}).")
                print("Check if your 'API_KEY' is valid or has been properly set.")
        except requests.exceptions.ConnectionError:
            print("Couldn't connect. Server could still start or the port is already in use.")
        else:
            return projects
        
    def label_studio_free_port(self, port: int):
        print(f"Checking if {port} is free...")
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                connections = proc.net_connections()
                for conn in connections:
                    if conn.laddr.port == port:
                        pid = proc.info['pid']
                        cmdline = proc.info['cmdline'] or []
                        cmdline_string = " ".join(cmdline).lower()

                        if "label-studio" in cmdline_string or "label_studio" in cmdline_string:
                            print(f"Old label studio session found on port: {port} (PID: {pid}). Closing safely...")
                            proc.terminate()
                            proc.wait(timeout=3)
                            print(f"Port: {port}, successfully closed.")

                            return (True, None)
                        
                        else:
                            print(f"Another process is running on port: {port}. Process: (PID: {pid}, Name: {proc.info['name']}).")

                            return (False, proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue

        return (True, None)


    def close(self):
        print("Gui is closed, cleaning up background progresses...")

        if self.running_process:
            if self.running_process.poll() is None:
                print("Label Studio process found. Ending sequence...")
                self.running_process.terminate()
                try:
                    self.running_process.wait(timeout=5)
                    print("Label Studio has successfully ended.")
                except subprocess.TimeoutExpired:
                    print("Label Studio isn't responding, force close...")
                    self.running_process.kill()
                    self.running_process.wait()
                    print("Forcefully closed Label Studio.")
                finally:
                    self.check_login = False
                    self.running_process = None
        
