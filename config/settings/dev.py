from .base import *

DEBUG = env('DEBUG', default=True)



# Database
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres://postgres:postgres@localhost:5432/django_boiler')
}
