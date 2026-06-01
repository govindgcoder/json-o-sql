from engine import JSONDB

DB = JSONDB("../users.json")

from typing import Any, Dict, List

from fastapi import FastAPI
from pydantic import BaseModel


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
