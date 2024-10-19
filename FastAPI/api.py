from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from routes.book import book_router
from routes.order import order_router
import os
from dotenv import load_dotenv
# import sys
# sys.path.append("..")

load_dotenv()
app = FastAPI()
app.include_router(book_router)
app.include_router(order_router)
@app.get('/')
async def root():
    # Redirect to docs
    return RedirectResponse(url='/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT)



if __name__ == '__main__':
    import uvicorn
    fastapi_host = os.environ.get('FASTAPI_HOST', str)
    fastapi_port = int(os.environ.get('FASTAPI_PORT', str))
    uvicorn.run(app, host=fastapi_host, port=fastapi_port)