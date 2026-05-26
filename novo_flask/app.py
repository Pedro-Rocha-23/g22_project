from flask import Flask, render_template, request, session
from classes.university import University
from classes.lab import Lab
from classes.grant import Grant
from classes.director import Director
from classes.uni_grant import Uni_grant
from subs.apps_gform import apps_gform
from subs.apps_subform import apps_subform
from subs.apps_analytics import apps_analytics

# ── Database path ──────────────────────────────────────────────────────────────
DB_PATH = 'data/g22_db.db'

# ── App setup ──────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = 'g22_secret_key'

# ── Load all classes from database ─────────────────────────────────────────────
University.read(DB_PATH)
Lab.read(DB_PATH)
Grant.read(DB_PATH)
Director.read(DB_PATH)
Uni_grant.read(DB_PATH)

# ── Home ───────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    stats = {
        'universities': len(University.obj),
        'labs':         len(Lab.obj),
        'grants':       len(Grant.obj),
        'directors':    len(Director.obj),
        'uni_grants':   len(Uni_grant.obj),
    }
    return render_template('index.html', stats=stats, ulogin=session.get('user'))

# ── Login / Logoff ─────────────────────────────────────────────────────────────
@app.route('/login')
def login():
    return render_template('login.html', resul='', ulogin=None)

@app.route('/chklogin', methods=['POST', 'GET'])
def chklogin():
    user     = request.form['user']
    password = request.form['password']
    # Simple hardcoded credentials — replace with Userlogin class if available
    USERS = {'root': '1234', 'user1': '1234'}
    if USERS.get(user) == password:
        session['user'] = user
        stats = {
            'universities': len(University.obj),
            'labs':         len(Lab.obj),
            'grants':       len(Grant.obj),
            'directors':    len(Director.obj),
            'uni_grants':   len(Uni_grant.obj),
        }
        return render_template('index.html', stats=stats, ulogin=session.get('user'))
    return render_template('login.html', resul='Invalid credentials', ulogin=None)

@app.route('/logoff')
def logoff():
    session.pop('user', None)
    return render_template('login.html', resul='', ulogin=None)

# ── Generic CRUD form — handles University, Lab, Grant, Director ───────────────
# Usage in navbar:  href="/gform/University"
#                   href="/gform/Director"   etc.
@app.route('/gform/<cname>', methods=['POST', 'GET'])
def gform(cname):
    if not session.get('user'):
        return render_template('login.html', resul='Please login first', ulogin=None)
    return apps_gform(cname)

# ── Subform — University (header) + Uni_grant (lines) ─────────────────────────
# Usage in navbar:  href="/subform/University_Uni_grant?option=''"
@app.route('/subform/<cname>', methods=['POST', 'GET'])
def subform(cname):
    if not session.get('user'):
        return render_template('login.html', resul='Please login first', ulogin=None)
    return apps_subform(cname)

# ── Analytics dashboard ────────────────────────────────────────────────────────
@app.route('/analytics')
def analytics():
    if not session.get('user'):
        return render_template('login.html', resul='Please login first', ulogin=None)
    return apps_analytics()

# ──────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
