from .base import *

DEBUG = env('DEBUG', default=True)



# Database
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgresql://postgres:postgres@localhost:5432/postgres')
}
