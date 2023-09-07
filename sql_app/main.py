import json
import pathlib
from typing import List, Union
from typing import Optional
from fastapi import FastAPI, Request, Header, Depends, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel

from . import models
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="sql_app/templates")

class developer(BaseModel):
    id: int
    dev_name: str
    duck1: str
    duck2: str

class duck(BaseModel):
    id: int
    duck_name: str
    size: str
    owner: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_populate_db():
    db = SessionLocal()

    num_developers = db.query(models.Developer).count()
    if num_developers == 0:
        developers = [
            {'id': '1', 'name': 'Tom', 'duck1': 'empty', 'duck2': 'empty'},
            {'id': '2', 'name': 'Eric', 'duck1': 'empty', 'duck2': 'empty'},    
            {'id': '3', 'name': 'Alice', 'duck1': 'empty', 'duck2': 'empty'},
            {'id': '4', 'name': 'Charlot', 'duck1': 'empty', 'duck2': 'empty'},
            {'id': '5', 'name': 'Bob', 'duck1': 'empty', 'duck2': 'empty'},    
            {'id': '6', 'name': 'Thomas', 'duck1': 'empty', 'duck2': 'empty'}
        ]
        for developer in developers:
            db.add(models.Developer(**developer))
        db.commit()
    else:
        print(f"{num_developers} developers are already in DB")

    num_ducks = db.query(models.Duck).count()
    if num_ducks == 0:
        ducks = [
            {'id': '1', 'name': 'Huey Duck', 'size': 'small', 'owner': 'empty'},
            {'id': '2', 'name': 'Dewey Duck', 'size': 'small', 'owner': 'empty'},
            {'id': '3', 'name': 'Louie Duck', 'size': 'small', 'owner': 'empty'},
            {'id': '4', 'name': 'Donald Duck', 'size': 'medium', 'owner': 'empty'},
            {'id': '5', 'name': 'Daisy Duck', 'size': 'medium', 'owner': 'empty'},
            {'id': '6', 'name': 'Scrooge McDuck', 'size': 'large', 'owner': 'empty'}
        ]
        for duck in ducks:
            db.add(models.Duck(**duck))
        db.commit()
    else:
        print(f"{num_ducks} ducks are already in DB")        
    

@app.get('/developers', response_class=HTMLResponse)
async def developer_index(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    developers = db.query(models.Developer).all()
    print(developers)
    context = {"request": request, "developers": developers}
    if hx_request:
        return templates.TemplateResponse("developers_table.html", context)
    return templates.TemplateResponse("developers.html", context)


@app.get('/ducks', response_class=HTMLResponse)
async def duck_index(
    request: Request, 
    hx_request: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    ducks = db.query(models.Duck).all()
    print(ducks)
    context = {"request": request, "ducks": ducks}
    if hx_request:
        return templates.TemplateResponse("ducks_table.html", context)
    return templates.TemplateResponse("ducks.html", context)


@app.post('/create/developer', response_class=HTMLResponse, status_code=201)
async def create_developer(developer: developer):
    db = SessionLocal()
    new_developer = {
        "id": developer.id,
        "name": developer.dev_name,
        "duck1": "empty",
        "duck2": "empty"
    }
    db.add(models.Developer(**new_developer))
    db.commit()


@app.post('/create/duck', response_class=HTMLResponse, status_code=201)
async def create_duck(duck: duck):
    db = SessionLocal()
    new_duck = {
        "id": duck.id,
        "name": duck.duck_name,
        "size": duck.size,
        "owner": "empty"
    }
    db.add(models.Duck(**new_duck))
    db.commit()


@app.delete('/delete/developer/{id}', status_code=204)
async def delete_developer(developer: developer):
    db = SessionLocal()
    delete_developer = {
        "id": developer.id,
        "name": developer.dev_name,
        "duck1": "empty",
        "duck2": "empty"
    }
    developers = db.query(models.Developer).all()
    test = developers[0]
    db.delete(models.Developer(**delete_developer))
    db.commit()

