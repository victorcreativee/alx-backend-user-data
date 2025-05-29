#!/usr/bin/env python3
"""Initializes the views Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *  # This must be here
from api.v1.views.session_auth import *
