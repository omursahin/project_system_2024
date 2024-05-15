# Create your tests here.
from pprint import pprint

from rest_framework import status
from rest_framework.test import APITestCase

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
        self.admin = MyUser.objects.create_user(email="test_admin@test.com", password=self.PASSWORD,
                                                identification_number="1234067892", is_admin=True)
        self.semester = Semester.objects.create(term="test", year=2023)
        self.course = Course.objects.create(code="test", title="test course", description="test description")
        self.semester_course = SemesterCourse.objects.create(semester=self.semester, course=self.course,
                                                             max_grup_size=88)

        self.semester2 = Semester.objects.create(term="test2", year=2022)
        self.course2 = Course.objects.create(code="test2", title="test2 course", description="test2 description")
        self.semester_course2 = SemesterCourse.objects.create(semester=self.semester, course=self.course,
                                                             max_grup_size=88)

    def test_group_creation_with_create(self):
        group_temp = {
            "title": "Test Group",
            "description": "test description",
            "max_size": 10,
        }
        group1 = Group.objects.create(
            owner=self.student,
            semester_course=self.semester_course,
            title=self.group_temp["title"],
            description=self.group_temp["description"])

        group2 = Group.objects.create(owner=self.student,
                                      semester_course=self.semester_course2,
                                      title=self.group_temp["title"],
                                      description=self.group_temp["description"],
                                      max_size=self.group_temp["max_size"],
                                      invitation_code=self.group_temp["invitation_code"])

        groups = Group.objects.filter(owner=self.student, semester_course=self.semester_course)
        self.assertLess(groups.count(), 2)

    def test_group_creation_with_post(self):
        group_temp = {
            "title": "Test Group",
            "description": "test description",
            "max_size": 10,
            "semester_course": self.semester_course.id
        }
        is_loggedin = self.client.login(email=self.student.email, password=self.PASSWORD)
        self.assertTrue(is_loggedin)

        response = self.client.post(self.GROUP_URL, group_temp)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)