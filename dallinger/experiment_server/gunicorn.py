from __future__ import absolute_import

from gunicorn.app.base import Application
from gunicorn import util
import multiprocessing
from dallinger.config import get_config
import os
import logging


class StandaloneServer(Application):
    def __init__(self):
        '''__init__ method
        Load the base config and assign some core attributes.
        '''
        self.load_user_config()
        self.usage = None
        self.callable = None
        self.prog = None
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.do_load_config()
        if 'OPENSHIFT_SECRET_TOKEN' in os.environ:
            my_ip = os.environ['OPENSHIFT_APP_DNS']
            public_interface = my_ip
        else:
            public_interface = self.options["bind"]
        self.logger.info("Now serving on {}".format(public_interface))

    def init(self, *args):
        '''init method
        Takes our custom options from self.options and creates a config
        dict which specifies custom settings.
        '''
        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg

    def load(self):
        '''load method
        Imports our application and returns it to be run.
        '''
        return util.import_app("dallinger.experiment_server.experiment_server:app")

    def load_user_config(self):
        config = get_config()
        workers = config.get("threads")
        if workers == "auto":
            workers = str(multiprocessing.cpu_count() * 2 + 1)

        self.loglevels = ["debug", "info", "warning", "error", "critical"]

        host = config.get("host")
        port = config.get("port")
        bind_address = "{}:{}".format(host, port)
        self.options = {
            'bind': bind_address,
            'workers': workers,
            'loglevels': self.loglevels,
            'loglevel': self.loglevels[config.get("loglevel")],
            'accesslog': config.get("Server Parameters", "logfile"),
            'errorlog': config.get("Server Parameters", "logfile"),
            'proc_name': 'psiturk_experiment_server',
            'limit_request_line': '0'
        }

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

def launch():
    config = get_config()
    config.load_config()
    # Setup logging
    LOG_LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR,
                  logging.CRITICAL]
    LOG_LEVEL = LOG_LEVELS[config.get('loglevel')]
    logging.basicConfig(format='%(asctime)s %(message)s', level=LOG_LEVEL)
    StandaloneServer().run()


if __name__ == "__main__":
    launch()
