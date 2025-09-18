import uvicorn

from src.core.config import settings
from src.server import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)
