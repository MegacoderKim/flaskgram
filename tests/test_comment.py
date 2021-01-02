from flask import url_for
from flask_jwt_extended import create_access_token
from socio.models import Comment


def test_get_comment(client, db, comment_factory, user_headers):
    # test 404 for missing comment
    comment_url = url_for("api.comment_by_id", comment_id='100000')
    rep = client.get(comment_url, headers=user_headers)
    assert rep.status_code == 404

    comment = comment_factory.create()
    db.session.commit()

    comment_url = url_for('api.comment_by_id', comment_id=comment.id)
    rep = client.get(comment_url, headers=user_headers)
    assert rep.status_code == 200

    comment_info = rep.get_json()["comment"]
    assert comment_info["body"] is not None


def test_only_owner_can_put_comment(client, db, comment_factory, auth_user, user_headers):
    comment = comment_factory.create()
    db.session.commit()

    comment_url = url_for('api.comment_by_id', comment_id=comment.id)
    new_comment_data = {'body': 'Updated body'}
    rep = client.put(comment_url, json=new_comment_data, headers=user_headers)
    assert rep.status_code == 400


def test_only_allowable_fields_can_be_updated(client, db, post_factory, auth_user, user_headers):
    post = post_factory.create()
    db.session.commit()

    comment = Comment(
        post_id=post.id,
        user_id=auth_user.id,
        body="Post body"
    )
    db.session.add(comment)
    db.session.commit()
    comment_url = url_for("api.comment_by_id", comment_id=comment.id)
    new_comment_data = {'body': 'This body has been updated', 'user_id': post.user.id}
    rep = client.put(comment_url, json=new_comment_data, headers=user_headers)
    assert rep.status_code == 400
    db.session.refresh(comment)
    assert comment.user_id == auth_user.id


def test_put_comment(client, db, post_factory, auth_user, user_headers):
    # test 404 for missing comment
    comment_url = url_for("api.comment_by_id", comment_id='100000')
    rep = client.put(comment_url, headers=user_headers)
    assert rep.status_code == 404
    # test comment update
    post = post_factory.create()
    db.session.commit()

    comment = Comment(
        post_id=post.id,
        user_id=auth_user.id,
        body="Post body"
    )
    db.session.add(comment)
    db.session.commit()
    comment_url = url_for("api.comment_by_id", comment_id=comment.id)
    new_comment_data = {'body': 'This body has been updated'}
    rep = client.put(comment_url, json=new_comment_data, headers=user_headers)
    assert rep.status_code == 200

    updated_comment = rep.get_json()["comment"]
    assert updated_comment['body'] == 'This body has been updated'


def test_delete_comment(client, db, post_factory, auth_user, user_headers):
    # test 404 missing comment
    comment_url = url_for("api.comment_by_id", comment_id='100000')
    rep = client.delete(comment_url, headers=user_headers)
    assert rep.status_code == 404

    post = post_factory.create()
    db.session.commit()

    comment = Comment(
        post_id=post.id,
        user_id=auth_user.id,
        body="Post body"
    )
    db.session.add(comment)
    db.session.commit()
    comment_url = url_for("api.comment_by_id", comment_id=comment.id)
    rep = client.delete(comment_url, headers=user_headers)
    assert rep.status_code == 200
    assert db.session.query(Comment).filter_by(id=comment.id).first() is None


def test_create_comment(client, db, post_factory, auth_user, user_headers):
    # test bad data
    comments_url = url_for('api.comments')
    data = {"body": "new comment"}
    rep = client.post(comments_url, json=data, headers=user_headers)
    assert rep.status_code == 400

    post = post_factory.create()
    db.session.commit()

    data["post_id"] = post.id
    data["user_id"] = auth_user.id

    rep = client.post(comments_url, json=data, headers=user_headers)
    assert rep.status_code == 201

    rep_data = rep.get_json()["comment"]
    assert rep_data["post_id"] == post.id
    assert rep_data["user_id"] == auth_user.id
    assert rep_data["body"] == "new comment"
    assert db.session.query(Comment).filter_by(id=rep_data["id"]).count() == 1


def test_list_comments(client, db, comment_factory, user_headers):
    comments_url = url_for('api.comments')
    comments = comment_factory.create_batch(5)

    db.session.add_all(comments)
    db.session.commit()

    rep = client.get(comments_url, headers=user_headers)
    results = rep.get_json()
    assert rep.status_code == 200
    for comment in comments:
        assert any(p["id"] == comment.id for p in results["results"])

    # test applying filter
    comment_url_filter = url_for('api.comments', post_id=comments[0].post_id)
    filtered_comment = client.get(comment_url_filter, headers=user_headers)
    results = filtered_comment.get_json()
    assert filtered_comment.status_code == 200
    assert len(results["results"]) == 1
