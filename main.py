import json
import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import StreamingResponse, FileResponse
from starlette.templating import Jinja2Templates
from db_na_kolenke import Message, db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("main.html", context={"request": request})


@app.get("/data_stream")
async def data_stream():
    return StreamingResponse(messages(), media_type="text/event-stream")


async def messages():
    message_dict = {
        "messages": [{
            "id": message.id,
            "username": message.name,
            "text": message.text
        } for message in Message.select()
        ]
    }

    yield json.dumps(message_dict)


@app.post("/send_message")
async def send_message(message_data: dict):
    username = message_data.get("username")
    text = message_data.get("text")
    message = Message.create(name=username, text=text)
    message.save()
    print(f"{username}: {text}")

    return {"status": "success"}


@app.get("/file/download")
def download_file():
    return FileResponse(
        path='/home/g4st3r/PycharmProjects/OtherProjects/huevii-marshrutizator-v2/'
             'api/styles/http_stackpath.bootstrapcdn.com_bootstrap_4.5.2_css_bootstrap.css',
    )


with db:
    db.create_tables([Message])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)
