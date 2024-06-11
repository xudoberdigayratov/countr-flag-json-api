import json
import aiofiles
import uvicorn
from fastapi import FastAPI, HTTPException
import logging

app = FastAPI()
data = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def load_data():
    global data
    async with aiofiles.open('data.json', 'r', encoding='utf-8') as outfile:
        content = await outfile.read()
        data = json.loads(content)
        logger.info("Data loaded successfully")


@app.on_event("startup")
async def startup_event():
    await load_data()


@app.get('/{code}')
async def get_country(code: str):
    if data is None:
        raise HTTPException(status_code=500, detail="Data not loaded")

    for x in data:
        if x['code'] == code:
            return x

    raise HTTPException(status_code=404, detail="Country not found")


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000, log_level='info')
