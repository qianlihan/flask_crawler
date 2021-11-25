# -*- coding: utf-8 -*-
from common.lib.UrlManager import UrlManager
from interceptors.errorHandler import *
from interceptors.Auth import *
from application import app
from controllers.index import index_page
from controllers.member import member_page

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

app.register_blueprint(index_page, url_prefix="/")
app.register_blueprint(member_page, url_prefix="/member")

app.add_template_global(UrlManager.build_Url, 'buildUrl')
app.add_template_global(UrlManager.build_static_Url, 'buildStaticUrl')
