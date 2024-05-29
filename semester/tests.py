# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import MyUser


class SemsterTest(APITestCase):
    SEMESTER_URL = "/api/v1/semesters/"

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

    def create_semester(self, isLogout):
        semester_detail = {
            "term": 'Bahar',
            "year": '2024',

        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_URL,
                                    semester_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        if (isLogout):
            self.client.logout()
        return response

    def test_add_records_not_logout(self):
        response = self.create_semester(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_records_logout(self):
        response = self.create_semester(isLogout=True)
        semester_detail = {
            "term": 'Bahar',
            "year": '2024',

        }
        response = self.client.post(self.SEMESTER_URL, semester_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def setUp(self):
        MyUser.objects.create_superuser(email=self.admin_user["email"],
                                        password=self.admin_user["password"],
                                        identification_number=self.admin_user["identification_number"])

        MyUser.objects.create_user(email=self.student_user["email"],
                                   password=self.student_user["password"],
                                   identification_number=self.student_user["identification_number"])

    def test_semester_create_admin(self):
        semester_detail = {
            "term": 'Bahar',
            "year": '2024',

        }
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_URL,
                                    semester_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_semester_list_admin(self):
        access = self.client.login(email=self.admin_user["email"], password=self.admin_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_semester_update_put_admin(self):
        response = self.create_semester(isLogout=False)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update_data = {
            "term": 'Bahar',
            "year": '2023',
        }
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_update_patch_admin(self):
        response = self.create_semester(isLogout=False)
        update_data = {
            "term": 'Güz',
        }
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_semester_delete_admin(self):
        response = self.create_semester(isLogout=False)
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

    def test_semester_not_create_student(self):
        semester_detail = {
            "term": 'Bahar',
            "year": '2024',
        }
        access = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertEqual(access, True)
        response = self.client.post(self.SEMESTER_URL,
                                    semester_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_not_list_student(self):
        access = self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        self.assertEqual(access, True)
        response = self.client.get(self.SEMESTER_URL)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_not_update_put_student(self):
        response = self.create_semester(isLogout=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update_data = {
            "term": 'Bahar',
            "year": '2023',
        }
        self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_not_update_patch_student(self):
        response = self.create_semester(isLogout=True)
        update_data = {
            "term": 'Güz',
        }
        self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_not_delete_student(self):
        response = self.create_semester(isLogout=True)
        self.client.login(email=self.student_user["email"], password=self.student_user["password"])
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_semester_not_create_unauthorized(self):
        semester_detail = {
            "term": 'Bahar',
            "year": '2024',

        }
        response = self.client.post(self.SEMESTER_URL,
                                    semester_detail, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_semester_not_list_unauthorized(self):
        response = self.client.get(self.SEMESTER_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_semester_unauthorized(self):
        response = self.create_semester(isLogout=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        update_data = {
            "term": 'Bahar',
            "year": '2023',
        }
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.put(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_semester_not_update_patch_unauthorized(self):
        response = self.create_semester(isLogout=True)
        update_data = {
            "term": 'Güz',
        }
        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.patch(url, update_data, format="json")
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_semester_not_delete_unauthorized(self):
        response = self.create_semester(isLogout=True)

        url = f"{self.SEMESTER_URL}{response.data['id']}/"
        response1 = self.client.delete(url)
        self.assertEqual(response1.status_code, status.HTTP_401_UNAUTHORIZED)
