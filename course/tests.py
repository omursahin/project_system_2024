# Create your tests here.
# TODO Şifre kontrolü gerçekleşmiyor
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import MyUser
from course.models import Course


class CourseTest(APITestCase):
    COURSE_URL = "/api/v1/courses/"
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
                                   identification_number=self.student_user["identification_number"])

    def test_login(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

    def test_create_course(self):
        test_course = Course.objects.create(code="test", title="test_title", description="test_description")
        self.assertEqual(test_course.code, "test")
        self.assertEqual(test_course.title, "test_title")
        self.assertEqual(test_course.description, "test_description")

    def test_create_course_endpoint_with_login(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response = self.client.get(self.COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_endpoint_without_login(self):
        self.client.logout()
        response = self.client.get(self.COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_is_course_unique(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response_1 = self.client.post(self.COURSE_URL, {"code": "123", "title": "123_title"})
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        response_2 = self.client.post(self.COURSE_URL, {"code": "123", "title": "123_title"})
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        pass
