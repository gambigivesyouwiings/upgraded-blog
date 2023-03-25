from pprint import pprint

from flask import Flask, render_template, request
import requests
import json
import smtplib

app = Flask(__name__)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
          }

response = requests.get(url='https://api.npoint.io/5808b1a3304a496f4c65')
blog = json.loads(response.text)
pprint(blog)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login("gambikimathi@gmail.com", "ibgkmojoitexczog")
        connection.sendmail("gambikimathi@gmail.com", "gambikimathi@gmail.com", email_message)


@app.route('/')
def home():
    return render_template('index.html', blog_posts=blog)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', check=False)
    if request.method == 'POST':
        form = request.form
        name = form['my-name']
        phone = form['my-num']
        email = form['my-email']
        message = form['my-message']
        send_email(name, email, phone, message)
        return render_template('contact.html', check=True)


@app.route('/blog<num>')
def get_blog(num):
    index = int(num) - 1
    return render_template('post.html', index=index, blog_post=blog)


# @app.route('/get-page', methods=['POST'])
# def get_page():
#     if request.method == 'POST':
#         name = request.form['myname']
#         print(name)
#     return f"<h1>{name}</h1>"


if __name__ == '__main__':
    app.run(debug=True)
