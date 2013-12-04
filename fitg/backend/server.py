import argparse
import service
import logging
import yaml
from rpyc.utils.server import ThreadedServer

parser = argparse.ArgumentParser()
parser.add_argument("--config", help="The config file to load", default="config.yaml", type=str)
args = parser.parse_args()

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("loading config file " + str(args.config))

with open (args.config, "r") as f:
    config = yaml.load(f)

t = ThreadedServer(service.FreedomService, hostname = config['host'], port = config['port'], logger=logger)
t.start()