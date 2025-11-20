import logging
import os
import sys


def get_logger(name: str) -> logging.Logger:
	logger = logging.getLogger(name)
	if not logger.handlers:
		handler = logging.StreamHandler(sys.stdout)
		fmt = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
		handler.setFormatter(fmt)
		logger.addHandler(handler)
	# add custom SUCCESS level between INFO (20) and WARNING (30)
	SUCCESS_LEVEL = 25
	if not hasattr(logging, "SUCCESS"):
		logging.SUCCESS = SUCCESS_LEVEL
		logging.addLevelName(SUCCESS_LEVEL, "SUCCESS")

		def success(self, message, *args, **kwargs):
			if self.isEnabledFor(SUCCESS_LEVEL):
				self._log(SUCCESS_LEVEL, message, args, **kwargs)

		logging.Logger.success = success
	# allow overriding via env var
	level_name = os.environ.get("LOG_LEVEL")
	try:
		if level_name:
			level = getattr(logging, level_name.upper(), logging.INFO)
		else:
			level = logging.INFO
	except Exception:
		level = logging.INFO

	logger.setLevel(level)
	return logger
