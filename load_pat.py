import os
from dotenv import load_dotenv

load_dotenv()
PAT_SOURCE = os.getenv("PAT_SOURCE")
PAT_TARGET = os.getenv("PAT_TARGET") 

print(f"Source PAT: {PAT_SOURCE}")
print(f"Target PAT: {PAT_TARGET}")
