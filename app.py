from flask import Flask, request, jsonify
from functools import wraps
from email_utils import send_email
import os

app = Flask(__name__)

# Load allowed IPs and domains from environment variables
allowed_ips_env = os.getenv("ALLOWED_IPS", "")
allowed_domains_env = os.getenv("ALLOWED_DOMAINS", "")

ALLOWED_IPS = set(ip.strip() for ip in allowed_ips_env.split(",") if ip.strip())
ALLOWED_DOMAINS = set(domain.strip() for domain in allowed_domains_env.split(",") if domain.strip())

def access_whitelist_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        origin = request.headers.get("Origin") or request.headers.get("Referer", "")
        print(f"Client IP: {client_ip}")
        print(f"Origin/Referer: {origin}")

        if client_ip in ALLOWED_IPS:
            return f(*args, **kwargs)

        if any(domain in origin for domain in ALLOWED_DOMAINS):
            return f(*args, **kwargs)

        return jsonify({"error": "Access denied: Your IP or domain is not allowed"}), 403

    return decorated_function

@app.route('/send-email', methods=['POST'])
@access_whitelist_required
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
