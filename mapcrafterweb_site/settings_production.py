from settings import *

# overriden later por supuesto
SECRET_KEY = "(na-jr+w8#tem2pvg@vvlphu4)7sesp%5+rz6d8r(7r5cgig-!"

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
