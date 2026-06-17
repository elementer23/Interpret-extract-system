import os
import subprocess
import time
import requests
from typing import Any
from src.utils.config import Config
import psutil
from src.error.error_hub import ErrorHub

url = f"http://localhost:{Config.get("port")}"
port = Config.get("port") if Config.get("port") else "8080"
api_key = Config.get("api_key")

class LabelStudioController():
    """
    Label Studio Controller is a class that handles the basic functionalities
    of the Label Studio API within the interpret-extract-system.

    It does not handle the actions within the Label Studio interface.
    """
    def __init__(self):
        self.running_process = None
        self.headers = {"Authorization": f"Token {api_key}",
                        "Content-Type": "application/json"
                       }
        self.api_allowed = False

    def label_studio_login(self, email: str, pwd: str):
        """
        This function allows the user to login in label studio.
        It does expect an email and password, but these don't have to exist inside the system just yet.
        This email and password are automatically used to sign-up, if they don't exist yet.
        """
        env_var = os.environ.copy()
        env_var["LABEL_STUDIO_USERNAME"] = email
        env_var["LABEL_STUDIO_PASSWORD"] = pwd
        env_var["LABEL_STUDIO_DISABLE_SIGNUP_WITHOUT_LINK"] = "true"
        env_var["LABEL_STUDIO_LOCAL_FILES_SERVING_ENABLED"] = "true"

        cmd = ["uvx", "--with", "label-studio", "--python", "3.12", "label-studio", "start", "--port", port]
        print("starting Label Studio in isolated Python 3.12 environment!")
        try:
            self.running_process = subprocess.Popen(cmd, env=env_var)

            print("Waiting for the initialization of the interface...")
            time.sleep(5)
        except Exception as e:
            ErrorHub.error_msg(f"Something went wrong while trying to start label studio: {e}", "warning")
            self.running_process = None

        if not api_key == "default":
            if self.__api_check():
                self.api_allowed = True 
        else:
            self.api_allowed = False
            return "You are logged in, but still haven't set your api key yet. Api privileges are restricted."

    def __api_check(self) -> bool:
        """
        This function makes a small api-call in order to check whether your api-key is present
        and whether the api key is valid or not. 
        """
        try:
            response = requests.get(f"{url}/api/projects", headers=self.headers)
            if response.status_code == 200:
                print("The given API key is valid for use, proper connection can be established!")
            else:
                ErrorHub.error_msg(f"Servers is working, API-verification failed (Status: {response.status_code}).", "information")
                return False 
        except requests.exceptions.ConnectionError:
            print("Couldn't connect. Server could still start or the port is already in use.") 
            return False
        else:
            return True

    def label_studio_projects(self):
        """
        This function returns the list of projects of the user, if the api-key is valid.
        """
        if not self.api_allowed: 
            ErrorHub.error_msg("Your api key hasn't been assigned yet or unable to connect to server.", "information")
            return None

        projects = None
        try:
            response = requests.get(f"{url}/api/projects", headers=self.headers)
            if response.status_code == 200:
                projects = response.json().get("results", [])
                print(f"successfully connected! Amount of projects present: {len(projects)}")
            else:
                print(f"Server is working, API-verification failed (Status: {response.status_code}).")
                print("Check if your 'API_KEY' is valid or has been properly set.")
        except requests.exceptions.ConnectionError:
            ErrorHub.error_msg("Couldn't connect. Server could still start or the port is already in use.", "warning")
        else:
            return projects
        
    def label_studio_free_port(self, port: int):
        """
        This function will free the given port, if label studio is already running on that port.
        If another progress is running on that port, a warning will be given. Telling the user
        to either close the process that is running or to try a different port.
        """
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

                            return True
                        else:
                            ErrorHub.error_msg(f"Another process is running on port: {port}. Process: (PID: {pid}, Name: {proc.info['name']}).", "warning")

                            return False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue

        return True

    def close(self):
        """
        This function closes anything related to label studio the moment
        that the label studio window is closed. Doing a force close.
        """
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
                    self.api_allowed = False
                    self.running_process = None
        
