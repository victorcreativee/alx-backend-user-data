#!/usr/bin/env python3
"""Creates Blueprint app_views"""
from flask import Blueprint
from api.v1.views import index

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
