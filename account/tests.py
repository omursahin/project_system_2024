# Create your tests here.
# TODO Şifre kontrolü gerçekleşmiyor
from rest_framework.test import APITestCase

from account.models import MyUser


class UserTest(APITestCase):
    USER_URL = "/api/v1/users/"
    LOGIN_URL = "/api/v1/account/token/"

    admin_user = {
        "email": "admin@test.com",
        "password": "123456",
        "identification_number": "1234567890"

    }

    student_user = {
        "email": "student@test.com",
        "password": "123456",
        "identification_number": "1234567891"

    }

    payload = {
        "email": "student@test.com",
        "password": "123456",
    }

    def setUp(self):
        MyUser.objects.create_superuser(email=self.admin_user["email"],
                                        password=self.admin_user["password"],
                                        identification_number=self.admin_user["identification_number"])
        MyUser.objects.create_user(email=self.student_user["email"],
                                   password=self.student_user["password"],
                                   identification_number=self.student_user
                                   ["identification_number"])

    def test_create_user_database(self):
        user = MyUser.objects.create_user(email="test_user@test.com",
                                          password="test1234",
                                          identification_number="1234567892")
        self.assertEqual(user.email, "test_user@test.com")

    def test_not_create_user_rest(self):
        response = self.client.post(self.USER_URL, self.payload)
        self.assertEqual(response.status_code, 401)

    def test_create_user_rest(self):
        user_detail = {
            "email": "new_user@test.com",
            "password": "123456",
            "identification_number": "1234567898"
        }
        access = self.login()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")
        response = self.client.post(self.USER_URL, user_detail)
        self.assertEqual(response.status_code, 201)

    def login(self, is_admin=True):
        payload = self.admin_user if is_admin else self.student_user
        response = self.client.post(self.LOGIN_URL, payload)
        self.assertEqual(response.status_code, 200)
        return response.data['data']['access']

    def tearDown(self):
        pass
