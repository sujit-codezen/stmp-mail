from flask import Flask, request, jsonify
from functools import wraps
from email_utils import send_email
import os

app = Flask(__name__)

# Load allowed IPs from .env and create a set
allowed_ips_env = os.getenv("ALLOWED_IPS", "")
ALLOWED_IPS = set(ip.strip() for ip in allowed_ips_env.split(",") if ip.strip())

def ip_whitelist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If behind proxy, you might want to check 'X-Forwarded-For'
        client_ip = request.remote_addr
        print(f"Client IP: {client_ip}")
        if client_ip not in ALLOWED_IPS:
            return jsonify({"error": "Access denied: Your IP is not allowed"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/send-email', methods=['POST'])
@ip_whitelist_required
def send_email_route():
    data = request.get_json()

    to = data.get('to')
    subject = data.get('subject')
    content = data.get('content')
    sender_account = data.get('sender_account', 'gmail1')
    attachments = data.get('attachments')

    if not to or not subject or not content:
        return jsonify({"error": "Missing required fields: 'to', 'subject', or 'content'"}), 400

    result = send_email(to, subject, content, sender_account, attachments)
    status_code = 200 if 'message' in result else 500
    return jsonify(result), status_code

if __name__ == '__main__':
    app.run(debug=True)
