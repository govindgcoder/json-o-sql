import json

def select_all(path):
    with open(path, "r") as f:
        data = json.load(f)
        return [
            obj for obj in data
        ]

def is_valid(obj, col, condition):
    if(obj.get(col) is None) return False
    sign, rhs = list(condition.items())[0]
    match sign:
        case "<":
            return obj.get(col)<rhs
        case ">":
            return obj.get(col)>rhs
        case "==":
            return obj.get(col)==rhs
        case "<=":
            return obj.get(col)<=rhs
        case ">=":
            return obj.get(col)>=rhs
        case "!=":
            return obj.get(col)!=rhs

def select_where(path, selected_columns, conditions):
    with open(path, "r") as f:
        data = json.load(f)
        return [
            {k: obj.get(k) for k in selected_columns if k in obj}
            for obj in data 
            if all(is_valid(obj,col,condition) for col,condition in conditions.items())
        ]

def insert(data, obj):
    with open(path, "r+") as f:
        data = json.load(f)
        data.append(obj)
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=4)

path = "../users.json"
    
print(select_where(path, ["age","department","name"], {"age": {"<":32}}))
    
obj = {"id": 5,
    "name": "GG",
    "age": 20,
    "department": "ceo"
}
insert(path,obj)
print(select_where(path, ["age","department","name"], {"age": {"<":32}}))




