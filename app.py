"Head file application"
import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

from exceptions import NotBoolConvertedType, NotIntConvertedType
from utils import build_query

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.post("/perform_query")
def perform_query():
    # нужно взять код из предыдущего ДЗ
    # добавить команду regex
    # добавить типизацию в проект, чтобы проходила утилиту mypy app.py
    data = request.json
    try:
        file_name: str = data['file_name']
        cmd1: str = data['cmd1']
        cmd2: str = data['cmd2']
        value1: str = data['value1']
        value2: str = data['value2']
    except:
        return BadRequest(description=f"Missing one or more arguments")

    path_file: str = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest(description=f"File {file_name} was not found")

    with open(path_file) as file:
        try:
            result = build_query(file, cmd1, value1)
            result = build_query(result, cmd2, value2)
            result = '\n'.join(result)
        except NotBoolConvertedType as e:
            return 'Method "sort" require a boolean parametr', 400
        except NotIntConvertedType as e:
            return 'Methods "limit" and "map" require a numeric parametr', 400

    return app.response_class(result, status='200 Completed successfully', content_type="text/plain")


if __name__ == '__main__':
    app.run(port=7777)
