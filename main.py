from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex
from waitress import serve

app = Flask(__name__)

@app.route("/parser", methods=["POST"])
def parser():
    try:
        data = request.get_json()
        latex_formula = data.get("formula", "")

        if not latex_formula:
            return jsonify({"error": "formula is required."}), 400

        expr = parse_latex(latex_formula)
        result = expr.doit()
        simplified_result = sp.simplify(str(result))

        response_data = {
            "formula": str(expr),
            "result": str(simplified_result)
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000) 