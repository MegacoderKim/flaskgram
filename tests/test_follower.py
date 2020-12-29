from flask import url_for

from socio.extensions import pwd_context
from socio.models import Follower


def test_get_follower(client, db, user_factory, user_headers):
    users = user_factory.create_batch(2)
    db.session.add_all(users)
    db.session.commit()

    user_ids = [x.id for x in users]

    follower1 = Follower(
        from_user_id=user_ids[0],
        to_user_id=user_ids[1]
    )

    db.session.add(follower1)
    db.session.commit()

    follower1_url = f'api/v1/followers/{follower1.id}'

    rep = client.get(follower1_url, headers=user_headers)
    assert rep.status_code == 200

    data = rep.get_json()["follower"]
    assert data["status"] == "pending"
    assert data["from_user_id"] == user_ids[0]
    assert data["to_user_id"] == user_ids[1]


def test_put_follower(client, db, user_factory, user_headers):
    # test 404
    missing_follower_link = url_for('api.follower_by_id', follower_id="20000")
    rep = client.put(missing_follower_link, headers=user_headers)
    assert rep.status_code == 404

    # test update follower records
    users = user_factory.create_batch(2)
    db.session.add_all(users)
    db.session.commit()
    user_ids = [x.id for x in users]

    follower = Follower(
        from_user_id=user_ids[0],
        to_user_id=user_ids[1]
    )
    db.session.add(follower)
    db.session.commit()

    update_date = {"status": "accepted"}

    follower_link = url_for('api.follower_by_id', follower_id=follower.id)
    rep = client.put(follower_link, json=update_date, headers=user_headers)
    assert rep.status_code == 200
    response_data = rep.get_json()["follower"]
    assert response_data["status"] == "accepted"
