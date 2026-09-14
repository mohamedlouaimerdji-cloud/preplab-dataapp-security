"""PrepLab web tier: deliberately weak, for assessment practice only.

Every weakness here is intentional and documented in lab/GUIDE.md. Do not copy
any of this into real code. Run only on your own machine.
"""
import hashlib, os
from flask import Flask, request, make_response, jsonify, render_template_string

app = Flask(__name__)

# WEAKNESS 1: secret in source / environment default, never rotated.
APP_SECRET = os.environ.get("APP_SECRET", "dev-secret-change-me")

# WEAKNESS 2: passwords stored as fast, unsalted SHA-256.
USERS = {
    "alice":  hashlib.sha256(b"password1").hexdigest(),
    "bob":    hashlib.sha256(b"guinness").hexdigest(),
    "admin":  hashlib.sha256(b"Dublin2026").hexdigest(),
    "svc-rep": hashlib.sha256(b"trustno1").hexdigest(),
}

# WEAKNESS 3: every account is effectively privileged; no least privilege.
ROLES = {u: "admin" for u in USERS}

RECORDS = {
    "1001": {"owner": "alice", "note": "Payroll summary Q3"},
    "1002": {"owner": "bob",   "note": "Supplier contract - Northwood"},
    "1003": {"owner": "admin", "note": "Board pack draft"},
}

PAGE = """<!doctype html><title>PrepLab</title>
<h1>PrepLab</h1>
<p>Deliberately weak target environment. Session 1 to 12.</p>
<ul>
  <li><code>POST /login</code> with <code>username</code> and <code>password</code></li>
  <li><code>GET  /record/&lt;id&gt;</code> (try changing the id)</li>
  <li><code>GET  /health</code></li>
  <li><code>GET  /debug</code></li>
</ul>"""

@app.get("/")
def index():
    return render_template_string(PAGE)

@app.post("/login")
def login():
    u = request.form.get("username", "")
    p = request.form.get("password", "")
    if u in USERS and USERS[u] == hashlib.sha256(p.encode()).hexdigest():
        resp = make_response(jsonify(ok=True, user=u, role=ROLES[u]))
        # WEAKNESS 4: session cookie with no HttpOnly, Secure or SameSite flags.
        resp.set_cookie("session", f"{u}:{APP_SECRET}")
        return resp
    return jsonify(ok=False), 401

@app.get("/record/<rid>")
def record(rid):
    # WEAKNESS 5: insecure direct object reference. No authorisation check at all:
    # any caller can read any record simply by changing the id.
    rec = RECORDS.get(rid)
    return (jsonify(rec), 200) if rec else (jsonify(error="not found"), 404)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.get("/debug")
def debug():
    # WEAKNESS 6: a debug endpoint exposing configuration, reachable unauthenticated.
    return jsonify(secret=APP_SECRET,
                   db_password=os.environ.get("DB_PASSWORD"),
                   users=list(USERS.keys()))

if __name__ == "__main__":
    # WEAKNESS 7: bound to all interfaces, debug mode on.
    app.run(host="0.0.0.0", port=5000, debug=True)
