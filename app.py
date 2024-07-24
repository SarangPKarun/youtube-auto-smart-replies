from flask import Flask, request, render_template, redirect, url_for
import comments

app = Flask(__name__)

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)