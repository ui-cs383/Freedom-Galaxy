import argparse
import pyconfig
import logging
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="The config file to load", default="config.yaml", type=str)
args = parser.parse_args()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("loading config file")

with open (args.config, "r") as f:
	config = yaml.load(f)

logger.info("setting up default values")

for key, value in config.items():
	pyconfig.set(key, value)

import service
from rpyc.utils.server import ThreadedServer

t = ThreadedServer(service.FreedomService, hostname = config['host'], port = config['port'], 
	logger=logger, protocol_config = {"allow_public_attrs" : True})
t.start()