#!/usr/bin/python3
import sys
import os
BASE_DIR = os.path.dirname(sys.argv[0])
# APP_PATH = os.path.dirname(sys.argv[0])
DB_NAME = os.path.join(BASE_DIR, 'magnit.sqlite')
APP_NAME = ''
SQL_PATH = os.path.join(BASE_DIR, 'sql/')
TEMPLATES = os.path.join(BASE_DIR, 'html/')
