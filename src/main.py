import os

import uvicorn

from src.config import load_config


def main():
    load_config()
    host = os.getenv("ALERTSENTRY_HOST", "127.0.0.1")
    port = int(os.getenv("ALERTSENTRY_PORT", "8000"))
    uvicorn.run("src.api.app:app", host=host, port=port, reload=True)


if __name__ == "__main__":
    main()
