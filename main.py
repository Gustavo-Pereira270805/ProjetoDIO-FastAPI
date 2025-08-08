from fastapi import FastAPI

from workout_api.routers.routers import api_router

app = FastAPI(title='ProjetoDIO')
app.include_router(api_router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='0.0.0.0', port=8000)
