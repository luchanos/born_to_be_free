from typing import Union

from asgiref.typing import ASGIApplication
from fastapi import FastAPI, Depends, Request
import uvicorn
import motor.motor_asyncio
import asyncio


async def setup_mongo(app: FastAPI):
    mongo_client = motor.motor_asyncio.AsyncIOMotorClient()
    app.state.mongo_client = mongo_client
    app.state.mongo_client.get_io_loop = asyncio.get_running_loop


def main() -> Union[ASGIApplication, FastAPI]:
    app = FastAPI(name="my_application")

    @app.on_event("startup")
    async def app_startup():
        await setup_mongo(app)

    async def get_user_item(request: Request, device_id: int) -> dict:
        db = request.app.state.mongo_client['test']
        document = await db.test.find_one({'a': 1})
        return {"device": 1}

    route_registrator = app.api_route(methods=["GET", ], path="/device/{device_id}")
    route_registrator(get_user_item)

    return app


if __name__ == "__main__":
    uvicorn.run(main())
