from rest_framework import status
from rest_framework.test import APITestCase

from account.models import MyUser
from course.models import Course
from semester.models import Semester
from semester_course.models import SemesterCourse


class SemesterCourseTest(APITestCase):
    REPORT_URL = "/api/v1/reports/"

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
        self.semester_course = SemesterCourse.objects.create(
            semester=self.semester,
            course=self.course,
            max_grup_size=100
        )

    def create_reports(self, isLogout):
        report_details = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": False,
            "is_final": False,

        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.post(self.REPORT_URL,
                                    report_details, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if (isLogout):
            access = self.client.logout()
        return response

    def test_create_report_not_logout(self):
        response = self.create_reports(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_report_logout(self):
        self.create_reports(isLogout=True)
        semester_course_detail = {
            "semester": self.semester.id,
            "course": self.course.id,
            "max_grup_size": 100,
        }
        response = self.client.post(self.REPORT_URL, semester_course_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reports_create_admin(self):
        response = self.create_reports(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_reports_not_create_student(self):
        report_detail = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": False,
            "is_final": False,
        }
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access,
                         True)
        response = self.client.post(self.REPORT_URL,
                                    report_detail)
        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_semester_course_create_unauthorized(self):
        report_detail = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": False,
            "is_final": False,
        }
        response = self.client.post(self.REPORT_URL,
                                    report_detail)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_list_admin(self):
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.REPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_report_list_student(self):
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.REPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report_list_unauthorized(self):
        response = self.client.get(self.REPORT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_delete_admin(self):
        response = self.create_reports(isLogout=False)
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

    def test_reportdelete_not_student(self):
        response = self.create_reports(isLogout=True)
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_report_delete_unauthorized(self):
        response = self.create_reports(isLogout=True)
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_semester_course_update_patch_admin(self):
        response = self.create_reports(isLogout=False)
        report_detail = {
            "is_public": True,

        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.patch(url, report_detail, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_course_not_update_patch_student(self):
        response = self.create_reports(isLogout=True)
        self.client.login(email=self.student_user["email"],
                          password=self.student_user["password"])
        report_detail = {

            "is_final": True,
        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.patch(url, report_detail, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_patch_unauthorized(self):
        response = self.create_reports(isLogout=True)
        report_detail = {

            "is_final": True,
        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.patch(url, report_detail, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    # Update-Put
    def test_semester_course_not_update_put_student(self):
        response = self.create_reports(isLogout=True)
        access = self.client.login(email=self.student_user["email"],
                                   password=self.student_user["password"])
        self.assertEqual(access, True)
        report_detail = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": True,
            "is_final": False,
        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.put(url, report_detail, format="json")

        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_update_put_admin(self):
        response = self.create_reports(isLogout=False)
        report_detail = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": True,
            "is_final": False,
        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.put(url, report_detail, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_course_update_put_unauthenticated(self):
        response = self.create_reports(isLogout=True)
        report_detail = {
            "semester_course": self.semester_course.id,
            "title": "Title1",
            "description": "Title1 Description",
            "is_public": True,
            "is_final": False,
        }
        url = f"{self.REPORT_URL}{response.data['id']}/"
        response1 = self.client.put(url, report_detail, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
