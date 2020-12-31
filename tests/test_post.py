from flask import url_for

from socio.models import Post


def test_get_post(client, db, user, user_headers):
    # test 404 for missing post
    post_url = url_for("api.post_by_id", post_id='100000')
    rep = client.get(post_url, headers=user_headers)
    assert rep.status_code == 404

    db.session.add(user)
    db.session.commit()

    post = Post(
        user_id=user.id,
        title="Post one",
        body="Post body",
    )
    db.session.add(post)
    db.session.commit()

    post_url = url_for('api.post_by_id', post_id=post.id)
    rep = client.get(post_url, headers=user_headers)
    assert rep.status_code == 200

    post_info = rep.get_json()["post"]
    assert post_info["title"] == "Post one"
    assert post_info["body"] == "Post body"
    # assert post_info["_links"] != None


def test_put_post(client, db, auth_user, user_headers):
    # test 404 for missing post
    post_url = url_for("api.post_by_id", post_id='100000')
    rep = client.put(post_url, headers=user_headers)
    assert rep.status_code == 404
    # test post update
    post = Post(
        user_id=auth_user.id,
        title='New Post',
        body='New Post Body'
    )
    db.session.add(post)
    db.session.commit()

    post_url = url_for('api.post_by_id', post_id=post.id)
    new_post_data = {'title': 'Update title', 'body': 'Updated body'}

    rep = client.put(post_url, json=new_post_data, headers=user_headers)
    assert rep.status_code == 200

    updated_post = rep.get_json()["post"]
    assert updated_post['title'] == 'Update title'
    assert updated_post['body'] == 'Updated body'


def test_only_owner_can_put_post(client, db, user, user_headers):
    db.session.add(user)
    db.session.commit()
    post = Post(
        user_id=user.id,
        title='Post',
        body='Post Body'
    )
    db.session.add(post)
    db.session.commit()

    post_url = url_for('api.post_by_id', post_id=post.id)
    new_post_data = {'title': 'Update title', 'body': 'Updated body'}

    rep = client.put(post_url, json=new_post_data, headers=user_headers)
    assert rep.status_code == 400


def test_delete_post(client, db, auth_user, user_headers):
    # test 404 missing post
    post_url = url_for("api.post_by_id", post_id='100000')
    rep = client.delete(post_url, headers=user_headers)
    assert rep.status_code == 404

    post = Post(
        user_id=auth_user.id,
        title='New Post',
        body='New post content'
    )
    db.session.add(post)
    db.session.commit()

    post_url = url_for('api.post_by_id', post_id=post.id)
    rep = client.delete(post_url, headers=user_headers)
    assert rep.status_code == 200
    assert db.session.query(Post).filter_by(id=post.id).first() is None


def test_create_post(client, db, auth_user, user_headers):
    # test bad data
    posts_url = url_for('api.posts')
    data = {"title": "new post"}
    rep = client.post(posts_url, json=data, headers=user_headers)
    assert rep.status_code == 400

    data["body"] = "new post body"
    data["user_id"] = auth_user.id

    rep = client.post(posts_url, json=data, headers=user_headers)
    assert rep.status_code == 201

    rep_data = rep.get_json()["post"]
    assert rep_data["title"] == "new post"
    assert rep_data["body"] == "new post body"

    assert db.session.query(Post).filter_by(id=rep_data["id"]).count() == 1


def test_list_posts(client, db, user_factory, user_headers):
    posts_url = url_for('api.posts')
    users = user_factory.create_batch(5)

    db.session.add_all(users)
    db.session.commit()

    posts = [Post(user_id=x.id, title=f'Post {x.id}', body=f'Body {x.id}') for x in users]
    db.session.add_all(posts)
    db.session.commit()

    rep = client.get(posts_url, headers=user_headers)
    results = rep.get_json()
    assert rep.status_code == 200
    for post in posts:
        assert any(p["id"] == post.id for p in results["results"])

    # test applying filter
    post_url_filter = url_for('api.posts', user_id=users[0].id)
    filtered_post = client.get(post_url_filter, headers=user_headers)
    results = filtered_post.get_json()
    assert filtered_post.status_code == 200
    assert len(results["results"]) == 1
