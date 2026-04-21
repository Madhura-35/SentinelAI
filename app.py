from flask import Flask, render_template, request
from textblob import TextBlob
import re

app = Flask(__name__)

def scan_content(text):
    # Phishing link detection
    links = re.findall(r'(https?://[^\s]+)', text)
    has_links = len(links) > 0
    
    # Analysis
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity # -1 to 1
    
    # Calculate safety percentage
    # -1 polarity = 0% safety, 1 polarity = 100% safety
    safety_percent = int(((sentiment + 1) / 2) * 100)
    
    if has_links:
        res = "Potential Phishing Link Detected 🛡️"
        status = "danger"
    elif sentiment < -0.4:
        res = "Toxic Content Detected ⚠️"
        status = "danger"
    elif sentiment < 0:
        res = "Negative Tone"
        status = "warning"
    else:
        res = "Content is Safe ✅"
        status = "success"
        
    return res, status, safety_percent, len(text), len(text.split())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    content = request.form['content']
    res, status, safety, chars, words = scan_content(content)
    
    return render_template('index.html', 
                           result=res, status=status, safety=safety, 
                           chars=chars, words=words, original=content)

if __name__ == '__main__':
    app.run(debug=True)