# Create your tests here.

import django.db.utils

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

    def test_create_course_is_unique(self):
        test_course_1 = Course.objects.create(code="test", title="test_title", description="test_description")
        self.assertEqual(test_course_1.code, "test")
        self.assertEqual(test_course_1.title, "test_title")
        self.assertEqual(test_course_1.description, "test_description")
        with self.assertRaises(django.db.utils.IntegrityError) as error:
            Course.objects.create(code="test", title="test_title", description="test_description")
            self.assertEqual(str(error), "UNIQUE constraint failed: course.code")

    def test_create_course_endpoint_with_admin_login_get(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response = self.client.get(self.COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_endpoint_with_student_user_login_get(self):
        is_logged_in = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(is_logged_in)

        response = self.client.get(self.COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course_endpoint_with_admin_login_post(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response = self.client.post(self.COURSE_URL,
                                    data={"code": "test",
                                          "title": "test_title",
                                          "description": "test_description"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_course_endpoint_with_student_user_login_post(self):
        is_logged_in = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(is_logged_in)

        response = self.client.post(self.COURSE_URL,
                                    data={"code": "test",
                                          "title": "test_title",
                                          "description": "test_description"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_endpoint_with_admin_login_patch(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response_created = self.client.post(self.COURSE_URL,
                                            data={"code": "test",
                                                  "title": "test_title",
                                                  "description": "test_description",
                                                  "is_active": True})
        self.assertEqual(response_created.status_code, status.HTTP_201_CREATED)

        response_patched = self.client.patch("{}{}{}".format(self.COURSE_URL, response_created.data["id"], "/"),
                                             data={"code": "test_patched",
                                                   "title": "test_title_patched",
                                                   "description": "test_description_patched"})
        self.assertEqual(response_patched.status_code, status.HTTP_200_OK)

    def test_create_course_endpoint_with_student_user_login_patch(self):
        is_logged_in_admin = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in_admin)

        response_created = self.client.post(self.COURSE_URL,
                                            data={"code": "test",
                                                  "title": "test_title",
                                                  "description": "test_description",
                                                  "is_active": True})
        self.assertEqual(response_created.status_code, status.HTTP_201_CREATED)

        self.client.logout()

        is_logged_in_user = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(is_logged_in_user)

        response_patched = self.client.patch("{}{}{}".format(self.COURSE_URL, response_created.data["id"], "/"),
                                             data={"code": "test_patched",
                                                   "title": "test_title_patched",
                                                   "description": "test_description_patched"})
        self.assertEqual(response_patched.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_endpoint_with_admin_login_del(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response_created = self.client.post(self.COURSE_URL,
                                            data={"code": "test",
                                                  "title": "test_title",
                                                  "description": "test_description",
                                                  "is_active": True})
        self.assertEqual(response_created.status_code, status.HTTP_201_CREATED)

        response_deleted = self.client.delete("{}{}{}".format(self.COURSE_URL, response_created.data["id"], "/"), )
        self.assertEqual(response_deleted.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_course_endpoint_with_student_user_login_del(self):
        is_logged_in_admin = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in_admin)

        response_created = self.client.post(self.COURSE_URL,
                                            data={"code": "test",
                                                  "title": "test_title",
                                                  "description": "test_description",
                                                  "is_active": True})
        self.assertEqual(response_created.status_code, status.HTTP_201_CREATED)

        self.client.logout()

        is_logged_in_user = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(is_logged_in_user)

        response_deleted = self.client.delete("{}{}{}".format(self.COURSE_URL, response_created.data["id"], "/"), )
        self.assertEqual(response_deleted.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_course_endpoint_without_login(self):
        self.client.logout()
        response = self.client.get(self.COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_is_course_unique_via_post(self):
        is_logged_in = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(is_logged_in)

        response_1 = self.client.post(self.COURSE_URL, {"code": "123", "title": "123_title"})
        self.assertEqual(response_1.status_code, status.HTTP_201_CREATED)
        response_2 = self.client.post(self.COURSE_URL, {"code": "123", "title": "123_title"})
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        pass
