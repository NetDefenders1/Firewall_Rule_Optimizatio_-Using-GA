from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/run-app', methods=['GET'])
def run_app():
    try:
        # Kill any existing Streamlit processes (optional, for ensuring single instance)
        subprocess.call("taskkill /F /IM streamlit.exe", shell=True)
        
        # Start the Streamlit app
        subprocess.Popen(["streamlit", "run", "app.py"], cwd=os.path.dirname(os.path.abspath(__file__)))
        return jsonify({"status": "success", "message": "Streamlit app is running"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
