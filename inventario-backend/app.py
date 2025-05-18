from flask import Flask, request, jsonify
from flask_cors import CORS
from schema import schema

app = Flask(__name__)
CORS(app)

@app.route("/graphql", methods=["POST", "GET"])
def graphql_api():
    if request.method == "GET":
        return "La API GraphQL está activa. Usa POST con el front en VUE, solo clonando y corriendo con npm run dev para consultas.", 200

    data = request.get_json()
    result = schema.execute(
        data.get("query"),
        variables=data.get("variables")
    )
    return jsonify(result.data)

if __name__ == "__main__":
    app.run(debug=True)
