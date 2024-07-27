from . import app
from flask import render_template, request, redirect
from models import Post, session


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/read_posts")
def read_all_posts():
    all_posts = session.query(Post).all()
    return render_template("index.html", all_posts=all_posts)


@app.route("/read_post_detail/<int:id>")
def read_post(id):
    post = session.query(Post).get(id)
    return render_template("post_detail.html", post=post)


@app.route("/create_post", methods=["POST", "GET"])
def create_post():
    if request.method == "POST":
        content = request.form["content"]
        title = request.form["title"]

        new_post = Post(
            title=title,
            content=content
        )

        try:
            session.add(new_post)
            session.commit()
            return redirect("/index")
        except Exception as exc:
            return f"При збереженні у поста виникла помилка: {exc}"
        finally:
            session.close()
    else:
        return render_template("create_post.html")


@app.route("/update_post/<int:id>", methods=["GET", "PUT"])
def update_post(id):
    post = session.query(Post).get(id)
    if request.method == "PUT":
        content = request.form["content"]
        title = request.form["title"]
        if title or content:
            try:
                post.title = title
                post.content = content
                session.commit()
                return redirect("/index")
            except Exception as exc:
                return f"При оновленні поста виникла помилка: {exc}"
            finally:
                session.close()
        else:
            return "Онови поля, оскільки ти їх не змінив/-ла"
    else:
        return render_template("create_post.html", post=post)


@app.route("/delete_post/<int:id>")
def delete_post(id):
    post = session.query(Post).filter_by(id=id)
    session.delete(post)
    session.close()
    return redirect("/index")


