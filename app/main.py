import os

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi import Response
from starlette.middleware.cors import CORSMiddleware
from app import schema
from app.base import CRUDBase
from app.models import QrNotes
from core.config import settings

db_url = 'sqlite:///' + settings.BASE_DIR + '\\sqllite.db' + '?check_same_thread=False'


def create_app():
    app = FastAPI()
    app.add_middleware(DBSessionMiddleware, db_url=db_url)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS.split(','),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = create_app()

base_qr = CRUDBase(QrNotes)


@app.get("/get_qr/{id}", )
def get_qr(id: str):
    return base_qr.get(id)


@app.get("/get_all_qr", )
def get_all():
    return base_qr.get_all()


@app.post("/create_qr", )
def create_qr(note: schema.QrNote):
    return base_qr.create(obj_in=note)


@app.put("/update_qr", )
def update_qr(note: schema.QrNote):
    db_obj = base_qr.get(note.id)
    return base_qr.update(obj_in=note, db_obj=db_obj)


@app.delete("/delete_qr/{id}", )
def delete_qr(id: str):
    base_qr.remove(id=id)
    return Response(status_code=200)
