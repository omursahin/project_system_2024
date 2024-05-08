from rest_framework.test import APITestCase
from semester_course_student.models import  SemesterCourseStudent
from account.models import MyUser
class SemesterCourseStudentTest(APITestCase):
    URL = '/api/v1/semester_course_students/'

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
        "is_active" : True,
        "mid_term" : 2025,
        "final" : 50,
        "make_up" : 70,
        "semester_course" : 1,
        "student" : 1
    }
    def setUp(self):
        MyUser.objects.create_superuser(email=self.admin_user["email"],
                                        password=self.admin_user["password"],
                                        identification_number=self.admin_user["identification_number"])
        MyUser.objects.create_user(email=self.student_user["email"],
                                   password=self.student_user["password"],
                                   identification_number=self.student_user["identification_number"])

    def test_post_user(self):
        self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        response = self.client.post(self.URL, self.payload)
        self.assertEqual(response.status_code, 200)


    def test_not_logged(self):
        fake_user = {
            "email": "fake_user@test.com",
            "password": "123456",
            "identification_number": "1234567898"
        }
        isLogged = self.client.login(email=fake_user["email"], password=fake_user["password"])
        self.assertFalse(isLogged)

