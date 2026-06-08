import torch
import warnings
import os
from dotenv import load_dotenv

load_dotenv()

warnings.filterwarnings(
    "ignore",
    message=".*'pin_memory' argument is set as true but no accelerator is found, then device pinned memory won't be used."
)

def get_device():

    cpu_forced = os.getenv("FORCE_CPU", "False").lower()

    if cpu_forced == "true":
        return torch.device("cpu")
    
    min_gb = float(os.getenv("MIN_GPU_GB", 7.0))

    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1e9
        if gpu_memory >= min_gb:
            return torch.device("cuda")
    return torch.device("cpu")

DEVICE = get_device()