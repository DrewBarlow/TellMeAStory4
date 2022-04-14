from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from tellmeastory.models import User, Post



def insertUser(usern: str , pw: str , dname: str) -> User:
    return User.objects.create(
        username=usern ,
        password=sha512(pw.encode("utf-8")).hexdigest() ,
        display_name=dname ,
    )


def insertStory(post_content: str , user_id: int) -> Post:
    return Post.objects.create(
        postText=post_content ,
        username_id=user_id ,
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
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)
        # Checks that a About John Doe page is loaded
        self.assertContains(res , dName + "'s Profile")

        # Checks to see that a story is created on the profile page
    def test_profile_page_with_story(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        userDB = User.objects.get(username=uName)
        userID = userDB.id

        sampleStoryText = "This is a sample story test"
        insertStory(sampleStoryText , userID)

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)
        # Checks that our story has successfully loaded
        self.assertContains(res , sampleStoryText)


        # Checks to ensure that the amount of stories that the user has created is correct and loaded
    def test_profile_story_count(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"

        insertUser(uName , pw , dName)

        userDB = User.objects.get(username=uName)
        userID = userDB.id

        sampleStoryText = "This is a sample story test"
        insertStory(sampleStoryText , userID)
        countStories = Post.objects.filter(username_id=userID).count()

        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks that the row with the number of stories has been successfully loaded
        self.assertContains(res , "<td>" + str(countStories) + "</td>")

        # Checks to make sure that the blurb has been loaded
    def test_profile_story_blurb(self) -> None:
        uName = TEST_ACCOUNT
        pw = "testing123"
        dName = "John Doe"
        blurb = "This is my users blurb"

        insertUser(uName , pw , dName)

        # Insert a blurb into the user
        userID = User.objects.get(username=uName).id
        User.objects.filter(
            id = userID,
        ).update(user_blurb = blurb)


        res: HttpResponse = self.client.get(URL_PROFILE + TEST_ACCOUNT + "/")
        # Checks that it loaded correctly
        self.assertEqual(res.status_code , 200)

        # Checks that the blurb is being successfully shown to the user
        self.assertContains(res, blurb)