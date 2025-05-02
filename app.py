# python -m flask run --host=0.0.0.0 --port=5002

from flask import Flask, send_file
from matrix import create_matrix
from rules import AttributeType, Rule, Ruletype
app = Flask(__name__)

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
    filename = "file.gif"
    return "OK!"
    # return send_file(filename, mimetype='image/gif')
    