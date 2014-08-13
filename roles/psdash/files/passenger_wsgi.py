import os
import os.path

# put the egg cache in passenger's ./tmp folder
os.environ['PYTHON_EGG_CACHE'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp')

from psdash.run import PsDashRunner
application = PsDashRunner.create_from_args().app

application.config['SECRET_KEY'] = 'ravioliravioligivemetheformuoli'
application.psdash.logs.add_patterns(['/var/log/nginx/access.log'])
