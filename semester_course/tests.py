from rest_framework import status
from rest_framework.test import APITestCase

from account.models import MyUser
from course.models import Course
from semester.models import Semester


class SemesterCourseTest(APITestCase):
    SEMESTER_COURSE_URL = "/api/v1/semester_courses/"
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
        self.semester = Semester.objects.create(term="Bahar", year=2000)
        self.course = Course.objects.create(code="CS101", title="Course1")

    def test_semester_course_create_admin(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100
        }
        access = self.client.login(email="admin@test.com",
                                   password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_semester_course_not_create_student(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100
        }
        access = self.client.login(email="student@test.com",
                                   password="123456")
        self.assertEqual(access,
                         True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_semester_course_create_unauthenticated(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100
        }
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_semester_course_list_admin(self):
        access = self.client.login(email="admin@test.com", password="123456")
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_list_student(self):
        access = self.client.login(email="student@test.com", password="123456")
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_delete_admin(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }

        access = self.client.login(email="admin@test.com",
                                   password="123456")
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(access, True)
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        print(url)
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

    def test_semester_course_delete_student(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }
        access = self.client.login(email="admin@test.com",
                                   password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access = self.client.logout()
        access = self.client.login(email="student@test.com", password="123456")
        self.assertEqual(access, True)
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_patch_admin(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }
        access = self.client.login(email="admin@test.com",
                                   password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update_data = {
            "max_group_size": 50
        }
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_course_update_patch_student(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }
        access = self.client.login(email="admin@test.com", password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access = self.client.logout()
        access = self.client.login(email="student@test.com", password="123456")
        update_data = {
            "max_group_size": 50
        }
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_put_student(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }
        access = self.client.login(email="admin@test.com", password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access = self.client.logout()
        self.assertEqual(access, None)
        access = self.client.login(email="student@test.com", password="123456")
        self.assertEqual(access, True)
        update_data = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 50
        }
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_put_admin(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 100,
        }
        access = self.client.login(email="admin@test.com", password="123456")
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update_data = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_group_size": 50
        }
        url = self.SEMESTER_COURSE_URL + f"{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
