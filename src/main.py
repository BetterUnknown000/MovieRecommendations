import subprocess
import sys
import time
import webbrowser
import urllib.request

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

server = subprocess.Popen(["py", "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true"])

time.sleep(3)
webbrowser.open("http://localhost:8501")
server.wait()
print("Streamlit server has stopped.")
sys.exit(0)