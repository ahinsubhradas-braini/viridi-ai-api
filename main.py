import uvicorn
from src.server import app
from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.port)