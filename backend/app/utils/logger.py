from loguru import logger

logger.add(
    "server.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO"
)