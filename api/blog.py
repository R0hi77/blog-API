from flask import Blueprint, request,g,session,jsonify
from flask_jwt_extended import jwt_required
from .database import get_db


blogbp = Blueprint("blog",__name__,url_prefix="/api/blog")




@blogbp.post('/create')
def create():
    title=request.form['title']
    body =request.form['body']
    author_id = request.form['id']
    error = None

    if not title:
        error = 'A title is required'
        
    elif not body:
        error = 'Enter a post body'
        
    if error is not None:
        return jsonify(
            {"message":error}

            )
    else:
        db = get_db()
        db.execute(
        'INSERT INTO post (title, body, author_id)'
        ' VALUES (?, ?,?)',
                (title, body, author_id))
        db.commit()
        return jsonify(

            {"message":"post created"}
        )
    

@blogbp.get('/all')
def all_posts():
    posts = get_db().execute(
       'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    for post in posts:
        return jsonify(
            {
                
                #"author_id" :post['author_id'],
                "created":post['created'],
                "title":post['title'],
                "body":post['body'],
                "username":post['username']

            }
    )




@blogbp.get('/<int:id>/one')
def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        return jsonify(
            {
                "message":"Post doesn't exist"
            }
        )

    return jsonify(
        {
            "username":post['username'],
            "title":post['title'],
            "body":post['body'],
            "created":post['created']
        }
    )
    


@blogbp.put('/<int:id>/update')
@jwt_required()
def single_post(id):
    post = get_db()
    post.execute(
        "SELECT * FROM post WHERE id = ?",(id,)
    ).fetchone()
    if post is None:
        return jsonify(
            {
                "message":"Post doesnt not exist"
            }
        )
    else:
        title = request.form['title']
        body = request.form['body']
        error = None
        if title is None:
            error ="Title is required"
            return jsonify(
                {
                    "message":error
                }
            )
        elif body is None:
            error = "Body is required "
            return jsonify(
                {
                    "message":error
                }
            )
        if error is None:
                db =get_db()
                db.execute(
                    "UPDATE post SET title =?, body=?"
                    " WHERE id = ?", (title,body,id)
                )
                db.commit()
                return jsonify(
                    {
                        "title":post['title'],
                        "body":post['body'],
                        "created":post['created']
                    }
                )
        

@blogbp.delete('/<int:id>/delete')
@jwt_required()
def delete_post(id):
    db=get_db()
    db.execute(
        "DELETE FROM post WHERE id = ?",(id)
    )
    db.commit()
    return jsonify(
        {
            "message":f"post with id {id} is deleted"
        }
    )



