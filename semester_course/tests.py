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

    def add_record(self, isLogout):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 100,
        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if (isLogout):
            access = self.client.logout()
        return response

    def test_add_records_not_logout(self):
        response = self.add_record(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_records_logout(self):
        response = self.add_record(isLogout=True)
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 100,
        }
        response = self.client.post(self.SEMESTER_COURSE_URL, semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Create
    def test_semester_course_create_admin(self):
        response = self.add_record(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_semester_course_not_create_student(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 100
        }
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access,
                         True)
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_semester_course_create_unauthorized(self):
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 100
        }
        response = self.client.post(self.SEMESTER_COURSE_URL,
                                    semester_course_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # List
    def test_semester_course_list_admin(self):
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_list_student(self):
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_course_list_unauthorized(self):
        response = self.client.get(self.SEMESTER_COURSE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # Delete
    def test_semester_course_delete_admin(self):
        response = self.add_record(isLogout=False)
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

    def test_semester_course_delete_not_student(self):
        response = self.add_record(isLogout=True)
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_delete_unauthorized(self):
        response = self.add_record(isLogout=True)
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    # Update-Patch
    def test_semester_course_update_patch_admin(self):
        response = self.add_record(isLogout=False)
        update_data = {
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_course_not_update_patch_student(self):
        response = self.add_record(isLogout=True)
        update_data = {
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_patch_unauthorized(self):
        response = self.add_record(isLogout=True)
        update_data = {
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    # Update-Put
    def test_semester_course_not_update_put_student(self):
        response = self.add_record(isLogout=True)
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        update_data = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")

        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_put_admin(self):
        response = self.add_record(isLogout=False)
        update_data = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_course_update_put_unauthenticated(self):
        response = self.add_record(isLogout=True)
        update_data = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 50
        }
        url = f"{self.SEMESTER_COURSE_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
