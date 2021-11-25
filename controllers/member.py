from application import app, db
from flask import Blueprint, request, make_response, redirect
from common.lib.Helper import ops_renderJSON, ops_renderErrJSON, ops_render
from common.lib.DataHelper import getCurrentTime
from common.lib.UrlManager import UrlManager
from common.models.user import User
from common.lib.UserService import UserService

member_page = Blueprint("member_page", __name__)


@member_page.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return ops_render("member/register.html")
    else:
        req = request.values
        nickname = req['nickname'] if "nickname" in req else ""
        login_name = req['login_name'] if "login_name" in req else ""
        login_pwd = req['login_pwd'] if "login_pwd" in req else ""
        login_pwd2 = req['login_pwd2'] if "login_pwd2" in req else ""
        if login_name is None or len(login_name) < 1:
            return ops_renderErrJSON(msg="invalid username")

        if login_pwd is None or len(login_pwd) < 6:
            return ops_renderErrJSON(msg="password is too short")

        if login_pwd != login_pwd2:
            return ops_renderErrJSON(msg="password not matched")

        user_info = User.query.filter_by(login_name=login_name).first()
        if user_info:
            return ops_renderErrJSON(msg="Username exists")

        model_user = User()
        model_user.login_name = login_name
        model_user.nickname = nickname if nickname is not None else login_name
        model_user.login_salt = UserService.geneSalt(8)
        model_user.login_pwd = UserService.genePwd(
            login_pwd, model_user.login_salt)
        model_user.create_time = model_user.update_time = getCurrentTime()
        db.session.add(model_user)
        db.session.commit()
        return ops_renderJSON(msg="Success")


@member_page.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return ops_render("member/login.html")
    else:
        req = request.values
        login_name = req['login_name'] if 'login_name' in req else ''
        login_pwd = req['login_pwd'] if 'login_pwd' in req else ''
        if login_name is None or len(login_name) < 1:
            return ops_renderErrJSON("username  is too short")

        if login_pwd is None or len(login_pwd) < 6:
            return ops_renderErrJSON("password is too short")
        user_info = User.query.filter_by(login_name=login_name).first()
        if not user_info:
            return ops_renderErrJSON("incorrect username")

        if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
            return ops_renderErrJSON("incorrect password")

        if user_info.status != 1:
            return ops_renderErrJSON("account locked")

        response = make_response(ops_renderJSON(msg="login success"))
        response.set_cookie(app.config['AUTH_COOKIE_NAME'],
                            "%s#%s" % (UserService.geneAuthCode(user_info), user_info.id), 60 * 60 * 24 * 120)
        return response


@member_page.route("/logout")
def logOut():
    response = make_response(redirect(UrlManager.build_Url("/")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
