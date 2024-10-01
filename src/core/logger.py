"""Custom logger."""

from sys import stdout

import loguru


def create_logger():  # type: ignore
    """Create custom logger."""
    loguru.logger.remove()
    loguru.logger.add(
        stdout,
        colorize=True,
        level="INFO",
        catch=True,
        format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | "
        + "<light-green>{level}</light-green>: "
        + "<light-white>{message}</light-white>",
    )
    return loguru.logger


LOGGER = create_logger()
