from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def home():
    return "<form action='/analize' method='post'><label>分析したい単語を入力<input type='text' name='tweet'></label><input type='submit' value='送信'></form>"

@app.route('/analize', methods=["POST"])
def analize():
    data = request.form["tweet"]
    return "<h1>分析結果</h1><h1>%s</h1><a href='/'>戻る</a>" % data

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)