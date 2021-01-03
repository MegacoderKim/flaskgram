from flask import url_for
from flask_jwt_extended import create_access_token
from socio.models import Like


def test_get_like(client, db, like_factory, user_headers):
    # test 404 for missing comment
    like_url = url_for("api.like_by_id", like_id='100000')
    rep = client.get(like_url, headers=user_headers)
    assert rep.status_code == 404

    like = like_factory.create()
    db.session.commit()

    like_url = url_for('api.like_by_id', like_id=like.id)
    rep = client.get(like_url, headers=user_headers)
    assert rep.status_code == 200

    comment_info = rep.get_json()["like"]
    assert comment_info["post_id"] is not None


def test_cannot_put_like(client, db, like_factory, auth_user, user_headers):
    # test 404 for missing like
    like_url = url_for("api.like_by_id", like_id='100000')
    rep = client.put(like_url, headers=user_headers)
    assert rep.status_code == 405
    # test like update
    like = like_factory.create()
    db.session.commit()
    like_url = url_for("api.like_by_id", like_id=like.id)
    like_data = {'user_id': 2}
    rep = client.put(like_url, json=like_data, headers=user_headers)
    assert rep.status_code == 405


def test_delete_like(client, db, post_factory, auth_user, user_headers):
    # test 404 missing comment
    comment_url = url_for("api.comment_by_id", comment_id='100000')
    rep = client.delete(comment_url, headers=user_headers)
    assert rep.status_code == 404

    post = post_factory.create()
    db.session.commit()

    like = Like(
        post_id=post.id,
        user_id=auth_user.id
    )
    db.session.add(like)
    db.session.commit()
    like_url = url_for("api.like_by_id", like_id=like.id)
    rep = client.delete(like_url, headers=user_headers)
    assert rep.status_code == 200
    assert db.session.query(Like).filter_by(id=like.id).first() is None


def test_create_like(client, db, post_factory, auth_user, user_headers):
    # test bad data
    likes_url = url_for('api.likes')
    data = {"user_id": 1}
    rep = client.post(likes_url, json=data, headers=user_headers)
    assert rep.status_code == 400

    post = post_factory.create()
    db.session.commit()

    data["post_id"] = post.id
    data["user_id"] = auth_user.id

    rep = client.post(likes_url, json=data, headers=user_headers)
    assert rep.status_code == 201

    rep_data = rep.get_json()["like"]
    assert rep_data["post_id"] == post.id
    assert rep_data["user_id"] == auth_user.id
    assert db.session.query(Like).filter_by(id=rep_data["id"]).count() == 1


def test_list_likes(client, db, like_factory, user_headers):
    likes_url = url_for('api.likes')
    likes = like_factory.create_batch(5)

    db.session.add_all(likes)
    db.session.commit()

    rep = client.get(likes_url, headers=user_headers)
    results = rep.get_json()
    assert rep.status_code == 200
    for like in likes:
        assert any(p["id"] == like.id for p in results["results"])

    # test applying filter
    like_url_filter = url_for('api.likes', post_id=likes[0].post_id)
    filtered_like = client.get(like_url_filter, headers=user_headers)
    results = filtered_like.get_json()
    assert filtered_like.status_code == 200
    assert len(results["results"]) == 1
