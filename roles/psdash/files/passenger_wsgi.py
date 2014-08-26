import os
import os.path

from psdash.run import PsDashRunner
application = PsDashRunner.create_from_args().app

application.config['SECRET_KEY'] = 'ravioliravioligivemetheformuoli'
application.psdash.logs.add_patterns(['/var/log/nginx/access.log'])
