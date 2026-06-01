from engine import JSONDB

DB = JSONDB("../users.json")

from typing import Any, Dict, List, Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserData(BaseModel):
    id: int
    name: str
    age: int
    department: str


class Operator(BaseModel):
    sign: Literal["<", ">", "==", "<=", ">=", "!="]
    value: Any


class Filter(BaseModel):
    field: str
    condition: Operator


class UpdateRequest(BaseModel):
    new_vals: Dict[str, Any]
    conditions: List[Filter]


class SelectRequest(BaseModel):
    selected_columns: List[str]
    conditions: List[Filter]


@app.post("/users/update")
def updateDB_where(request: UpdateRequest):
    result = DB.update_where(
        new_vals=request.new_vals,
        conditions={
            f.field: {f.condition.sign: f.condition.value} for f in request.conditions
        },
    )
    if result:
        return {"status": "success"}
    return {"status": "failure"}


@app.get("/users/")
def select_all():
    try:
        return DB.select_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users/query")
def select_where(request: SelectRequest):
    try:
        return DB.select_where(
            selected_columns=request.selected_columns,
            conditions={
                f.field: {f.condition.sign: f.condition.value}
                for f in request.conditions
            },
        )

    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/users/")
def insert(request: UserData):
    try:
        DB.insert(request.model_dump())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
