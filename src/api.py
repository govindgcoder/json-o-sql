from engine import JSONDB

DB = JSONDB("../users.json")

from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserData(BaseModel):
    id: int
    name: str
    age: int
    department: str


class Operator(BaseModel):
    sign: str
    value: Any


class Filter(BaseModel):
    field: str
    condition: Operator


class UpdateRequest(BaseModel):
    new_vals: Dict[str, Any]
    conditions: List[Filter]


@app.post("/update/")
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
