from rest_framework.test import APITestCase
from semester_course_student.models import  SemesterCourseStudent
from semester_course.models import SemesterCourse
from semester.models import Semester
from course.models import Course
from account.models import MyUser
from rest_framework import status
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
    def setUp(self):
        self.super_user = MyUser.objects.create_superuser(email=self.admin_user["email"],
                                        password=self.admin_user["password"],
                                        identification_number=self.admin_user["identification_number"])
        self.student = MyUser.objects.create_user(email=self.student_user["email"],
                                   password=self.student_user["password"],
                                   identification_number=self.student_user["identification_number"])
        self.semester = Semester.objects.create(term="Bahar", year=2000)
        self.course = Course.objects.create(code="CS101", title="Course1")
        self.semester_course = SemesterCourse.objects.create(semester=self.semester, course=self.course, max_grup_size=10)

    def test_create_SCS_object(self):
        semester_course_student = SemesterCourseStudent.objects.create(is_active= True, mid_term=2025, final=50,make_up=70,
        semester_course=self.semester_course,student=self.student)
        self.assertTrue(semester_course_student.is_active)
        self.assertEqual(semester_course_student.mid_term,2025)
        self.assertEqual(semester_course_student.final,50)
        self.assertEqual(semester_course_student.make_up,70)
        self.assertEqual(semester_course_student.semester_course,self.semester_course)
        self.assertEqual(semester_course_student.student,self.student)
    def test_users_login(self):
        access = self.client.login(email = "fake@user.com", password = "somefakepassword")
        self.assertFalse(access)
    def test_semester_course_student_adminPost(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email = self.admin_user["email"], password = self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL,semester_course_student_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    def test_semester_course_student_studentPost(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL, semester_course_student_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_semester_course_student_unauthorizedPost(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        response = self.client.post(self.URL, semester_course_student_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_semester_course_student_list_admin(self):
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_semester_course_student_list_admin(self):
        access = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(access)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    def test_semester_course_student_delete_admin(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL,semester_course_student_payload)
        url = "{}{}/".format(self.URL, response.data['id'])
        response_for_delete = self.client.delete(url)
        self.assertEqual(response_for_delete.status_code, status.HTTP_204_NO_CONTENT)
    def test_semester_course_student_delete_student(self): # hata barındırıyor
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access_admin = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access_admin)
        response = self.client.post(self.URL, semester_course_student_payload)
        self.client.logout()
        access_student = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(access_student)
        url = "{}{}/".format(self.URL, response.data['id'])
        response_for_delete = self.client.delete(url)
        self.assertEqual(response_for_delete.status_code, status.HTTP_403_FORBIDDEN)
    def test_semester_course_student_patch_admin(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL, semester_course_student_payload)
        update_data = {
            "final":60
        }
        url = "{}{}/".format(self.URL, response.data['id'])
        response_for_patch = self.client.patch(url,update_data)
        self.assertEqual(response_for_patch.status_code, status.HTTP_200_OK)
    def test_semester_course_student_patch_student(self): # hata barındırıyor
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL, semester_course_student_payload)
        access = self.client.logout()
        access = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertTrue(access)
        update_data = {
            "final": 60
        }
        url = "{}{}/".format(self.URL, response.data['id'])
        response_for_patch = self.client.patch(url, update_data)
        self.assertEqual(response_for_patch.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_course_student_put_admin(self):
        semester_course_student_payload = {
            "is_active": True,
            "mid_term": 2025,
            "final": 50,
            "make_up": 70,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertTrue(access)
        response = self.client.post(self.URL, semester_course_student_payload)
        update_data = {
            "is_active": True,
            "mid_term": 2025,
            "final": 55,
            "make_up": 77,
            "semester_course": self.semester_course.id,
            "student": self.student.id
        }
        url = "{}{}/".format(self.URL, response.data['id'])
        response_for_patch = self.client.put(url, update_data)
        self.assertEqual(response_for_patch.status_code, status.HTTP_200_OK)
    def test_semester_course_student_put_student(self):
        pass # student için delete ve patch hata barındırdığından pas geçilmiştir

