from flask import Flask, request, jsonify, render_template
import pandas as pd
import re

app = Flask(__name__)

# Load the Excel file
df = pd.read_excel(r"C:\Users\shash\Downloads\DATA FOR FIRST AID.xlsx")

def wildcard_search(df, column_name, pattern):
    regex_pattern = pattern.replace("?", ".").replace("*", ".*")
    return df[df[column_name].str.contains(regex_pattern, flags=re.IGNORECASE, regex=True, na=False)]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "")
    if query:
        matches = wildcard_search(df, "Emergency Issue", query + "*")
        suggestions = matches["Emergency Issue"].unique().tolist()
    else:
        suggestions = []
    return jsonify(suggestions)

@app.route("/first_aid")
def first_aid():
    issue = request.args.get("issue", "")
    row = df[df["Emergency Issue"].str.lower() == issue.lower()]
    if not row.empty:
        return jsonify(row.iloc[0]["First Aid"])
    return jsonify("No first aid instructions found.")

if __name__ == "__main__":
    app.run(debug=True)
