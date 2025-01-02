import json


class JsonLoader:
    def __init__(self, filepath: str):
        self.json = None
        self.load_json(filepath)

    def load_json(self, filepath: str):
        with open(filepath, encoding="utf-8") as file:
            self.json = json.load(file)

    def get_json(self, key: str):
        """从json中查找键，返回值"""
        if key in self.json:
            return self.json[key]
