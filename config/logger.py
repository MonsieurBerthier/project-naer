import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout,
           colorize=True,
           format="<level>{time:DD/MM/YYYY HH:mm:ss} | {level: <7} | {name}.{function}()@{line} : {message}</level>")
