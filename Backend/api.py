from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from configurations.logger import logger
from seeds.book import seed_router
from routes.book import book_router
from routes.order import order_router
from dotenv import load_dotenv

logger.info("Starting API...", func_name=__name__)
load_dotenv()

app = FastAPI(title="Library API", version="1.0.1")
@app.get('/')
async def root():
    # Redirect to docs
    return RedirectResponse(url='/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT)
app.include_router(book_router)
app.include_router(order_router)
app.include_router(seed_router)

# if __name__ == '__main__':
#     import uvicorn
#     fastapi_host = os.environ.get('FASTAPI_HOST', str)
#     fastapi_port = int(os.environ.get('FASTAPI_PORT', str))
#     uvicorn.run(app, host=fastapi_host, port=fastapi_port)