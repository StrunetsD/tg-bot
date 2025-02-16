from flask import Flask
from flask import render_template, redirect, request, url_for, session
from flask_admin import AdminIndexView, expose
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import logging
from core.config import SYNC_DATABASE_URL, SECRET_KEY, ADMIN_PASSWORD, ADMIN_USERNAME
from database.models import User, UserQuery, FailedRequest

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SYNC_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.before_request
def require_admin_login():
    if request.path.startswith('/admin') and request.endpoint != 'login_admin' and not session.get("admin_logged_in"):
        logger.info("Unauthorized access attempt to admin area.")
        return redirect(url_for("login_admin"))

class HomeView(AdminIndexView):
    def is_accessible(self):
        return session.get("admin_logged_in")

    def inaccessible_callback(self, name, **kwargs):
        logger.warning("Admin area access denied.")
        return redirect(url_for("login_admin"))

    @expose('/')
    def index(self):
        users_count = db.session.query(func.count(User.id)).scalar()
        queries_count = db.session.query(func.count(UserQuery.id)).scalar()
        failed_queries_count = db.session.query(func.count(FailedRequest.id)).scalar()
        stats = {
            "users_count": users_count,
            "queries_count": queries_count,
            "failed_queries_count": failed_queries_count
        }

        logger.info("Admin dashboard accessed.")
        return self.render("home.html", stats=stats)

@app.route("/", methods=['GET'])
def index():
    return redirect(url_for("login_admin"))

@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            logger.info(f"Admin logged in: {username}")
            return redirect(url_for("admin.index"))
        else:
            logger.warning(f"Failed login attempt for username: {username}")

    return render_template("login_admin.html")
