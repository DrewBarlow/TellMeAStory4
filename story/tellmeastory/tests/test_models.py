from django.test import TestCase
from TellMeAStory4.story.tellmeastory.models import User, Post, Report, Ban

class UserModelTests(TestCase):
    def test_valid_username(self) -> None:
        """
        is_valid_username() should return False if the desired
        username contains anything other than Unicode word chars,
        numbers, spaces, hyphens, or underscores.
        Similarly, the username should have a length of 5 <= name <= 14.
        """
        invalid_name_bang: str = "Woah!"
        invalid_name_short: str = "hey"
        invalid_name_long: str = "0123456789TenEleven"
        valid_name: str = "GodHimself"

        bang: User = User(username=invalid_name_bang)
        short: User = User(username=invalid_name_short)
        long: User = User(username=invalid_name_long)
        valid: User = User(username=valid_name)

        self.assertIs(bang.is_valid_username(), False)
        self.assertIs(short.is_valid_username(), False)
        self.assertIs(long.is_valid_username(), False)
        self.assertIs(valid.is_valid_username(), True)

        return

    def test_unique_username_checking(self) -> None:
        """
        is_unique_username() should return False if the desired
        username is not registered to another user account.
        """
        desired_dup_name: str = "Cringe"
        desired_uniq_name: str = "NotCringe"

        orig_user: User = User(username=desired_dup_name)
        orig_user.save()
        dup_user: User = User(username=desired_dup_name)
        new_orig_user: User = User(username=desired_uniq_name)

        self.assertIs(dup_user.is_unique_username(), False)
        self.assertIs(new_orig_user.is_unique_username(), True)

        return

    def test_valid_display_name(self) -> None:
        """
        is_valid_display_name() should return False if the desired
        display name does not have a length of 5 <= name <= 20.
        """
        invalid_too_short: str = ":)"
        invalid_too_long: str = "Not smile because that would be too short"
        valid: str = "God Himself"

        short: User = User(display_name=invalid_too_short)
        long: User = User(display_name=invalid_too_long)
        good: User = User(display_name=valid)

        self.assertIs(short.is_valid_display_name(), False)
        self.assertIs(long.is_valid_display_name(), False)
        self.assertIs(good.is_valid_display_name(), True)

        return

class testDatabaseRetrieval(TestCase):
    #testing Post database functionality
    def test_get_retrieval_post(self):

        # create objects
        user1 = User.objects.create(username="user1", password="test", display_name = "Warrior", admin = False )
        user2 = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)


        # create some objects
        Post.objects.create(username=user1, post_id="4ad56262a25", postText="My first post!")
        Post.objects.create(username=user2, password="26q2aa263a2", postText="My second post!")

        # get by the post_id (primary key)
        first_post = Post.objects.get(post_id="4ad56262a25",)
        second_post = Post.objects.get(post_id="26q2aa263a2")

        #check if the text is equal in the database
        self.assertEqual(first_post.postText, "My first post!")
        self.assertEqual(second_post.postText, "My second post!")

        return

    #testing UserTable database functionality
    def test_get_retrieval_user(self):

        # create objects
        User.objects.create(username="user1", password="test", display_name="Warrior", admin=False)
        User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)


        #get by the user_id (primary key)
        first_post = User.objects.get(username="user1")
        second_post = User.objects.get(username="user2")

        #check if the passwords are equal
        self.assertEqual(first_post.password, "qwertyuiop")
        self.assertEqual(second_post.password, "oagkawdoa")

        return

class testReporting(TestCase):
    def test_report(self):

        #create objects
        user1 = User.objects.create(username="user1", password="test", display_name="Warrior", admin=False)
        user2 = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)

        # create some objects
        Post.objects.create(username=user2, post_id="4ad56262a25", postText="My first post!")

        report = Report.objects.create(reporting_username=user1,reported_id="9205a925",report_reason="Racism",id_for_report="6a92agh0aw",post=user2)


        self.assertEqual(report.report_reason, "Racism")

        return

    def test_ban(self):

        # create some objects
        user = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)

        Post.objects.create(username=user, post_id="4ad56262a25", postText="My first post!")

        #simulate a ban
        Ban.objects.create(bannedUser=str(user))

        User.delete(User.objects.get(username=str(user)))

        #check if the current user is in the User table and Ban table
        get_user = User.objects.filter(username=str(user))
        get_banned_user = Ban.objects.filter(bannedUser=str(user))

        self.assertEqual(get_user,None)
        self.assertNotEqual(get_banned_user, None)

        return



