from flask import Flask, request, render_template, redirect, url_for
import comments
import threading

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form.get('video_url')
        if video_url:
            # Run in a separate thread to not block the Flask server
            # Note: This will pop up a browser on the Server (User's PC)
            t = threading.Thread(target=comments.process_video_comments, args=(video_url,))
            t.start()
            return "Bot started! Check the terminal/browser popup to log in."
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)