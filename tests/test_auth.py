def test_revoke_access_token(client, user_headers):
    resp = client.delete("/auth/revoke_access", headers=user_headers)
    assert resp.status_code == 200

    resp = client.get("/api/v1/users", headers=user_headers)
    assert resp.status_code == 401


def test_revoke_refresh_token(client, user_refresh_headers):
    resp = client.delete("/auth/revoke_refresh", headers=user_refresh_headers)
    assert resp.status_code == 200

    resp = client.post("/auth/refresh", headers=user_refresh_headers)
    assert resp.status_code == 401
