import uvicorn
from src.config import load_config

def main():
    load_config()
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
