from flask import Flask, render_template, request
import requests
import smtplib

my_email = "YOUR EMAIL ADDRESS"
my_password = "YOUR EMAIL PASSWORD"

posts = requests.get("https://api.npoint.io/e29a1617eac310cb7bd5").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():

    if request.method == "POST":
        user_email = request.form["email"]
        message = request.form["message"]
        username = request.form["name"]
        phone = request.form["phone"]
        send_email(username,user_email,phone,message)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

def send_email(username, user_email, phone, message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:New Message\n\nName: {username}\nEmail: {user_email}\nPhone: {phone}\nMessage:{message}"
        )



if __name__ == "__main__":
    app.run(debug=True)
