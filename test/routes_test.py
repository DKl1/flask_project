from flask_testing import TestCase
from main import app
import unittest


class MyTest(TestCase):

    def create_app(self):
        return app


class RoutesTest(MyTest):
    URL = "http://localhost:8080/"

    def setUp(self):
        self.del_id = 59
        self.post_id = 61
        self.update_id = 3
        self.id_room = 3
        self.username = "klym2123456789101232"
        self.admin = "roma123456", "romaromaroma"
        self.wrong_admin = "maksym", "romaromaroma"

    def test_get_room_by_number(self):
        resp = self.client.get("{}{}".format(RoutesTest.URL, 'rooms/?room_number=1'))
        self.assertEqual(resp.status_code, 200)

    def test_update_room(self):
        resp = self.client.put("{}{}".format(RoutesTest.URL, 'rooms/?room_number=' + str(self.update_id)),
                               auth=self.admin, json={
                "bed_n": 3,
                "description": "descriptiondescriptiondescription",
                "people": 3,
                "photo_url": "https://www.google.com/url?sa=is%3A%2F%2Fwww.ritzcarlton",
                "price": 540,
                "room_number": self.update_id,
                "type": "comfort"
            })
        self.assertEqual(resp.status_code, 200)
        resp = self.client.put("{}{}".format(RoutesTest.URL, 'rooms/?room_number=' + str(self.update_id)),
                               auth=self.admin, json={
                "bed_n": 3,
                "description": "",
                "people": 3,
                "photo_url": "https://www.google.com/url?sa=is%3A%2F%2Fwww.ritzcarlton",
                "price": 540,
                "room_number": self.update_id,
                "type": "comfort"
            })
        self.assertEqual(resp.status_code, 400)

    def test_delete_room(self):
        resp = self.client.delete("{}{}".format(RoutesTest.URL, "rooms/"+str(self.del_id)), auth=self.admin)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.delete("{}{}".format(RoutesTest.URL, "rooms/" + str(42)), auth=self.admin)
        self.assertEqual(resp.status_code, 404)

    def test_get_rooms(self):
        resp = self.client.get("{}{}".format(RoutesTest.URL, 'rooms'))
        self.assertEqual(resp.status_code, 200)

    def test_post_room(self):
        resp = self.client.post("{}{}".format(RoutesTest.URL, 'rooms'),
                                auth=self.admin, json={
                "bed_n": 5,
                "description": "descriptiondescriptiondescriptiondescriptiondescriptiondescription",
                "people": 3,
                "photo_url": "https://www.google.com/url?sa=is%3A%2F%2Fwww.ritzcarlton",
                "price": 5400,
                "room_number": self.post_id,
                "type": "comfort"
            })
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post("{}{}".format(RoutesTest.URL, 'rooms'),
                                auth=self.admin, json={
                "bed_n": 5,
                "description": "",
                "people": 3,
                "photo_url": "ritzcarlton",
                "price": 5400,
                "room_number": 1,
                "type": "comfort"
            })
        self.assertEqual(resp.status_code, 400)

    def test_add_reserve(self):
        resp = self.client.post("{}{}".format(RoutesTest.URL, 'rooms/reserve/'),
                                auth=self.admin, json={
                "reservation_id": self.post_id,
                "full_name": "KLym Danylo",
                "phone": "+380680898745",
                "date_from": "2023-05-12",
                "date_to": "2023-06-12",
                "id_room": self.id_room,
            })
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post("{}{}".format(RoutesTest.URL, 'rooms/reserve/'),
                                auth=self.admin, json={
                "reservation_id": self.post_id,
                "full_name": "",
                "phone": "+38068089874l",
                "date_from": "2023-05-12",
                "date_to": "2023-06-12",
                "id_room": self.id_room,
            })
        self.assertEqual(resp.status_code, 400)

    def test_get_reserve(self):
        resp = self.client.get("{}{}".format(RoutesTest.URL, 'rooms/reserve/'))
        self.assertEqual(resp.status_code, 200)

    def test_post_admin(self):
        resp = self.client.post("{}{}".format(RoutesTest.URL, 'admin'), auth=self.admin, json={
            "admin_id": self.post_id,
            "full_name": "Klym Danylo",
            "username": self.username,
            "password": "danylodanylodanylo"
        })
        self.assertEqual(resp.status_code, 200)
        resp_er422 = self.client.post("{}{}".format(RoutesTest.URL, 'admin'), auth=self.admin, json={
            "admin_id": self.post_id,
            "full_name": "Klym Danylo",
            "username": "klym123456",
            "password": "danylodanylodanylo"
        })
        self.assertEqual(resp_er422.status_code, 422)
        resp_er400 = self.client.post("{}{}".format(RoutesTest.URL, 'admin'), auth=self.admin, json={
            "admin_id": 1,
            "full_name": "K",
            "username": self.username,
            "password": "danylodanylodanylo"
        })
        self.assertEqual(resp_er400.status_code, 400)

    def test_get_admin(self):
        resp = self.client.get("{}{}".format(RoutesTest.URL, 'admin?admin_id=1'), auth=self.admin)
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get("{}{}".format(RoutesTest.URL, 'admin?admin_id=1'), auth=self.wrong_admin)
        self.assertEqual(resp.status_code, 401)


if __name__ == '__main__':
    unittest.main()
