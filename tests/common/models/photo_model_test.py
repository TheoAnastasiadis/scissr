from src.common.models import Photo


def test_create_photo():
    photo_data = {
        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
        "url": "/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
        "public": True,
    }
    photo = Photo(**photo_data)
    assert photo.id == photo_data["_id"]
    assert photo.url == photo_data["url"]
    assert photo.public == photo_data["public"]


def test_default_public():
    photo = Photo(
        _id="066de609-b04a-4b30-b46c-32537c7f1f6e",
        url="/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
    )
    assert not photo.public


def test_allow_population_by_field_name():
    photo_data = {
        "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
        "url": "/066de609-b04a-4b30-b46c-32537c7f1f6e.jpg",
        "public": True,
    }
    photo = Photo(**photo_data)
    assert photo.id == photo_data["_id"]
