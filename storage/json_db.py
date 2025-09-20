import json
import os
from typing import List, Dict, Any


class JsonDB:
    def __init__(self, data_dir: str):
        self.data_dir = data_dir


    def _path(self, name: str) -> str:
        return os.path.join(self.data_dir, f'{name}.json')


    def exists(self, name: str) -> bool:
        return os.path.exists(self._path(name))


    def read(self, name: str) -> List[Dict[str, Any]]:
        path = self._path(name)
        if not os.path.exists(path):
            return []
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


    def write(self, name: str, rows: List[Dict[str, Any]]):
        with open(self._path(name), 'w', encoding='utf-8') as f:
            json.dump(rows, f, ensure_ascii=False, indent=2)


    def upsert(self, name: str, row: Dict[str, Any], key: str):
        rows = self.read(name)
        found = False
        for i, r in enumerate(rows):
            if r.get(key) == row.get(key):
                rows[i] = row
                found = True
            break
        if not found:
            rows.append(row)
        self.write(name, rows)