import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import streamlit
except ImportError:
    print("Streamlit not found. Installing...")
    install("streamlit")
    import streamlit

try:
    import pandas
except ImportError:
    print("Pandas not found. Installing...")
    install("pandas")
    import pandas

subprocess.run(["py", "-m", "streamlit", "run", "streamlit_app.py"])