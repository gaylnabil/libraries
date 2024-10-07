from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from routes.book import book_router

app = FastAPI()
app.include_router(book_router)

@app.get('/')
async def root():
    # Redirect to docs
    return RedirectResponse(url='/docs', status_code=status.HTTP_307_TEMPORARY_REDIRECT)



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)