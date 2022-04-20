from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User
from tellmeastory.models import Post

URL_PROFILE = "/profile/"
TEST_ACCOUNT = "tellme1"


def insertUser(usern: str , pw: str , dname: str) -> User:
    return User.objects.create(
        username=usern ,
        password=sha512(pw.encode("utf-8")).hexdigest() ,
        display_name=dname ,
    )


class navBarTests(TestCase):


    # Tests to make sure Login and Register are displayed on the navbar.
    def test_login_register(self)->None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")

        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to ensure that Login and Register are displayed
        self.assertContains(res, "Login")
        self.assertContains(res, "Register")

    def test_myaccount_myprofile(self)-> None:

        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName,
            "password": pw
        })

        res: HttpResponse = self.client.get("/story/account/" + TEST_ACCOUNT + "/")

        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        #Checks to make sure that the profile page is addressed
        self.assertContains(res, "My Profile")

        # Checks to ensure that a welcome message is given
        self.assertContains(res , "Welcome")

    def test_myaccount_manage(self)-> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })

        res: HttpResponse = self.client.get("/story/account/" + TEST_ACCOUNT + "/")


        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to make sure that a manage page is properly displayed
        self.assertContains(res , "Manage")

    def test_myaccount_attempt_other_account(self)-> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        extraAccount = "thetest1"

        insertUser(uName , pw , dName)
        insertUser(extraAccount, pw, dName + " Second")

        resLogin: HttpResponse = self.client.post("/story/login/" , data={
            "username": uName ,
            "password": pw
        })

        res: HttpResponse = self.client.get("/story/account/" + extraAccount + "/")

        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks to make sure an Oh No! message is displayed to the user
        self.assertContains(res, "Oh no!")



