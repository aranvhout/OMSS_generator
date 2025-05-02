# python -m flask run --host=0.0.0.0 --port=5002

from flask import Flask, send_file, Response
import zipfile
import io
from werkzeug.wsgi import FileWrapper
from matrix import create_matrix
from rules import AttributeType, Rule, Ruletype
from PIL import Image

app = Flask(__name__)

def toPng(arr):
    img = Image.fromarray(arr)
    membuf = io.BytesIO()
    img.save(membuf, format="png") 
    membuf.seek(0)
    return membuf.getvalue()

@app.route("/")
def home():
    r1 = {
    'BigShape': [
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SHAPE, value = 'square'),
        Rule(Ruletype.PROGRESSION, AttributeType.ANGLE),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.COLOR, value = 'blue'),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.NUMBER),
        Rule(Ruletype.FULL_CONSTANT, AttributeType.SIZE)]}


    solution_matrix, problem_matrix, alternatives = create_matrix(r1, alternatives=4, seed = None,  alternative_seed =None ,save = False, entity_types=[ 'BigShape',])

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr("problem_matrix.png", toPng(problem_matrix))
        for idx, alternative in enumerate(alternatives):
             zip_file.writestr('alternative_0{}.png'.format(idx), toPng(alternative))
    zip_buffer.seek(0)

    file_wrapper = FileWrapper(zip_buffer)
    headers = {
        'Content-Disposition': 'attachment; filename="{}"'.format('file.zip')
    }
    response = Response(file_wrapper,
                        mimetype='application/zip',
                        direct_passthrough=True,
                        headers=headers)
    return response
    # return send_file("problem.zip", mimetype='image/gif')
    