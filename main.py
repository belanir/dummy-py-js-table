from flask import Flask, render_template_string, jsonify, request, send_file
import pandas as pd
import numpy as np
import io

app = Flask(__name__)

AUTO_REFRESH_INTERVAL = 300000
PAGE_TITLE = "Some Title"
COLUMNS = ["Name", "Age", "City"] + [f"Col{i}" for i in range(1, 11)]

def generate_dataframe():
    np.random.seed(0)
    names = np.random.choice(['Ana', 'Bruno', 'Carlos', 'Daniela', 'Eduardo'], size=100)
    ages = np.random.randint(18, 65, size=100)
    cities = np.random.choice(['São Paulo', 'Rio de Janeiro', 'Belo Horizonte', 'Curitiba', 'Porto Alegre'], size=100)
    extra_cols = {f"Col{i}": np.random.randn(100).round(2) for i in range(1, 11)}
    return pd.DataFrame({"Name": names, "Age": ages, "City": cities, **extra_cols})[COLUMNS]


def generate_details(field, value):
    np.random.seed(hash(value) % 2 ** 32)
    n = np.random.randint(1, 6)
    return pd.DataFrame(
        {"Name": [value] * n, "Order": np.arange(1, n + 1), "Amount": np.random.uniform(100, 1000, size=n).round(2)})


@app.route("/")
def index():
    with open("index.html", 'r', encoding='utf-8') as f:
        content = f.read()
        return render_template_string(content, title="Some Title", interval=AUTO_REFRESH_INTERVAL, page_lenght=50) #possible values:[50, 100, 200, 500, -1]


@app.route("/data")
def get_data():
    df = generate_dataframe()
    return jsonify(df.to_dict(orient="records"))


@app.route("/details")
def details():
    field = request.args.get("field")
    value = request.args.get("value")
    if not field or not value:
        return jsonify([])
    df_details = generate_details(field, value)
    return jsonify(df_details.to_dict(orient="records"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
