import logging
import os
from app import create_app, db
from app.models import User, Product, Feedback

# generate app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')

logger = logging.getLogger('mylogger')
logger.setLevel((logging.INFO))

fh = logging.FileHandler('test.log')
fh.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter('[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('this is a info')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Product=Product, Feedback=Feedback)


if __name__ == '__main__':
    # main app
    app.run(debug=True, port=3389)
