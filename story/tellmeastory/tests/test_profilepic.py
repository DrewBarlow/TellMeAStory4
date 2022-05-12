from django.http import HttpResponse
from django.test import TestCase
from tellmeastory.models import User, Account
from hashlib import sha512
from django.db.models import ImageField
from tellmeastory.forms import ProfileForm
from django.core.files.uploadedfile import SimpleUploadedFile


def insertUser(usern: str, dname: str, pic: str) -> Account:
    return Account.objects.create(
        username=usern,
        display_name=dname,
        profile_pic=pic
    )

URL_PROFILE = "/profile/"
TEST_ACCOUNT = "tellme1"

class ProfilePageTests(TestCase):

    # Checks to see if the page returns a does not exist page for a profile.
    def test_profile_page_not_exist(self) -> None:
        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks to make sure the page loaded correctly
        self.assertEqual(res.status_code , 200)
        # Checks to make sure a did not find account message has been created
        self.assertContains(res , "You have tried to access an account page that does not exist.")

        # Checks to see if the page shows the profile of the user
    def test_profile_page_account_exists(self) -> None:
        uName = TEST_ACCOUNT
        dName = "John Doe"
        pPic = "https://i.ibb.co/MnjnjFL/profile-pic.jpg"

        insertUser(uName, dName, pPic)

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)
        # Checks that a About John Doe page is loaded
        self.assertContains(res , dName + "'s Profile")
        # Checks that a profile pic is loaded
        self.assertContains(res, pPic)

        
