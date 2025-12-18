def test_home_page_renders() -> None:
    from app.pages.home import render_home

    html = render_home()
    assert "__SERVICE_NAME__" not in html
    assert "/notifications" in html
    assert "Load latest notifications" in html
