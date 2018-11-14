import os
import sys
import site

site.addsitedir(os.path.join(os.path.dirname(__file__), 'env/local/lib/pyhon2.7/site-packages'))

sys.path.append('/var/www/cracker')

activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

from app import app as application
