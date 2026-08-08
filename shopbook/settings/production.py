import os
from .base import *  # noqa: F403,F401

DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
