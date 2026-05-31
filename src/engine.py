import json


class JSONDB:
    def __init__(self, value):
        self.path = value

    def select_all(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return [obj for obj in data]

    @staticmethod
    def is_valid(obj, col, condition):
        if obj.get(col) is None:
            return False

        sign, rhs = list(condition.items())[0]
        match sign:
            case "<":
                return obj.get(col) < rhs
            case ">":
                return obj.get(col) > rhs
            case "==":
                return obj.get(col) == rhs
            case "<=":
                return obj.get(col) <= rhs
            case ">=":
                return obj.get(col) >= rhs
            case "!=":
                return obj.get(col) != rhs

    def select_where(self, selected_columns, conditions):
        with open(self.path, "r") as f:
            data = json.load(f)
            return [
                {k: obj.get(k) for k in selected_columns if k in obj}
                for obj in data
                if all(
                    self.is_valid(obj, col, condition)
                    for col, condition in conditions.items()
                )
            ]

    def update_where(self, new_vals, conditions):
        with open(self.path, "r+") as f:
            data = json.load(f)
            for obj in data:
                if all(
                    self.is_valid(obj, col, condition)
                    for col, condition in conditions.items()
                ):
                    for key, val in new_vals.items():
                        obj[key] = val
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

    def delete_where(self, conditions):
        with open(self.path, "r+") as f:
            data = json.load(f)
            new_data = [
                obj
                for obj in data
                if not all(
                    self.is_valid(obj, col, condition)
                    for col, condition in conditions.items()
                )
            ]
            f.seek(0)
            f.truncate()
            json.dump(new_data, f, indent=4)

    def insert(self, obj):
        with open(self.path, "r+") as f:
            data = json.load(f)
            data.append(obj)
            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)
