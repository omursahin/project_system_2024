from rest_framework import status
from rest_framework.test import APITestCase

from semester_course_student.models import SemesterCourseStudent
from .models import Group
from semester_course.models import SemesterCourse
from account.models import MyUser
from semester.models import Semester
from course.models import Course


class GroupTest(APITestCase):
    GROUP_URL = "/api/v1/groups/"
    PASSWORD = "test1234"



    def setUp(self):
        self.student = MyUser.objects.create_user(email="test_user@test.com", password=self.PASSWORD,
                                                  identification_number="1234567892")
        self.admin = MyUser.objects.create_superuser(email="test_admin@test.com", password=self.PASSWORD,
                                                identification_number="1234067892", is_admin=True)

        self.semester = Semester.objects.create(term="test", year=2023)
        self.course = Course.objects.create(code="test", title="test course", description="test description")
        self.semester_course = SemesterCourse.objects.create(semester=self.semester, course=self.course,
                                                             max_grup_size=3)
        self.semester_course_student = SemesterCourseStudent.objects.create(semester_course=self.semester_course,
                                                                            student=self.student, mid_term=80, final= 70)

        self.semester2 = Semester.objects.create(term="test2", year=2022)
        self.course2 = Course.objects.create(code="test2", title="test2 course", description="test2 description")
        self.semester_course2 = SemesterCourse.objects.create(semester=self.semester, course=self.course,
                                                             max_grup_size=3)

    def test_group_creation_with_create(self):
        group_temp = {
            "title": "Test Group",
            "description": "test description",
            "max_size": 10,
        }
        group1 = Group.objects.create(
            owner=self.student,
            semester_course=self.semester_course,
            title=group_temp["title"],
            description=group_temp["description"],
            max_size=group_temp["max_size"])

        group2 = Group.objects.create(
            owner=self.student,
            semester_course=self.semester_course2,
            title=group_temp["title"],
            description=group_temp["description"],
            max_size=group_temp["max_size"])

        groups = Group.objects.filter(owner=self.student, semester_course=self.semester_course)
        self.assertLess(groups.count(), 2)

    def test_group_creation_with_post(self):
        group_temp = {
            "title": "Test Group",
            "description": "test description",
            "semester_course": self.semester_course.id
        }
        is_logged_in = self.client.login(email=self.student.email, password=self.PASSWORD)
        self.assertTrue(is_logged_in)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

    def test_student_cannot_create_multiple_groups(self): #ogrenci birden fazla grup olusturamaz
        group_temp = {
            "title": "Test Group 1",
            "description": "test description",
            "semester_course": self.semester_course.id
        }
        is_logged_in = self.client.login(email=self.student.email, password=self.PASSWORD)
        self.assertTrue(is_logged_in)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

        group_temp["title"] = "Test Group 2"
        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_admin_can_create_multiple_groups(self):   #admin birden fazla grup olusturabilir
        group_temp = {
            "title": "Admin Test Group 1",
            "description": "admin test description",
            "semester_course": self.semester_course.id
        }
        is_logged_in = self.client.login(email=self.admin.email, password=self.PASSWORD)
        self.assertTrue(is_logged_in)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

        group_temp["title"] = "Admin Test Group 2"
        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)

    def test_student_must_be_enrolled_in_course_to_create_group(self):
        group_temp = {
            "title": "Test Group",
            "description": "test description",
            "semester_course": self.semester_course2.id  # Öğrencinin kayıtlı olmadığı kurs
        }
        is_logged_in = self.client.login(email=self.student.email, password=self.PASSWORD)
        self.assertTrue(is_logged_in)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)


    def test_cannot_create_group_if_max_groups_reached(self):

        Group.objects.create(title="Group 1", description="desc", semester_course=self.semester_course,
                             owner=self.admin, max_size=10)
        Group.objects.create(title="Group 2", description="desc", semester_course=self.semester_course,
                             owner=self.admin, max_size=10)
        Group.objects.create(title="Group 3", description="desc", semester_course=self.semester_course,
                             owner=self.admin, max_size=10)
        group_temp = {
            "title": "Test Group 4",
            "description": "test description",
            "semester_course": self.semester_course.id,
            "max_size": 10
        }
        is_logged_in = self.client.login(email=self.student.email, password=self.PASSWORD)
        self.assertTrue(is_logged_in)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)