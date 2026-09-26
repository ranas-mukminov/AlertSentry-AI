import logging
import logging.config
import yaml
import os


def setup_logging(
    config_path: str = "config/logging.yaml",
    default_level: int = logging.INFO,
    env_key: str = "LOG_CFG",
) -> None:
    """
    Setup logging configuration
    """
    path = os.getenv(env_key, config_path)
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            except Exception as e:
                print(f"Error loading logging config: {e}")
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print(f"Logging config file not found at {path}. Using default config.")


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
