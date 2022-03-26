from django.http import HttpResponse
from django.test import TestCase
from hashlib import sha512
from .models import User

class UserRegistrationModelTests(TestCase):
    def test_valid_username(self) -> None:
        """
        is_valid_username() should return False if the desired
        username contains anything other than lower/upper english letters,
        numbers, spaces, hyphens, or underscores.
        Similarly, the username should have a length of 5 <= name <= 14.
        TODO: Make more inclusive for other languages.
        """
        invalid_name_bang: str = "Woah!"
        invalid_name_short: str = "hey"
        invalid_name_long: str = "0123456789TenEleven"
        valid_name: str = "God Himself"

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

class UserRegistrationViewTests(TestCase):
    def test_blank_registration_page(self) -> None:
        """
        Base registration page should have no error messages present.
        """
        res: HttpResponse = self.client.get("/story/register/")
        self.assertEqual(res.status_code, 200)
        self.assertNotContains(res, "Invalid ")
        self.assertNotContains(res, "already taken.")

        return

    def test_registration_all_fields(self) -> None:
        """
        Enter a valid username, password, and display name into each field.
        Should redirect to /story/login/ and the User should be in the db.
        The input password should be hashed, so it will not be equal to what is in the db.
        In this case, User.username can, but should not, == User.display_name.
        """
        inp_name: str = "Spongebob"
        inp_pass: str = "!1Aaaaa"
        inp_dname: str = "Spongey Boy"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "display_name": inp_dname
        })

        # HTTP 302 -> Redirect (Found)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), "/story/login/")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertNotEqual(new_user, None)
        self.assertEqual(new_user.username, inp_name)
        self.assertEqual(new_user.display_name, inp_dname)
        self.assertNotEqual(new_user.password, inp_pass)
        self.assertEqual(new_user.password, sha512(inp_pass.encode("utf-8")).hexdigest())

        return

    def test_registration_no_display_name(self) -> None:
        """
        Enter a valid username and password into their fields.
        Should redirect to /story/login/ and the User should be in the db.
        The input password should be hashed, so it will not be equal to what is in the db.
        In this case, User.username == User.display_name.
        """
        inp_name: str = "Spongebob"
        inp_pass: str = "!1Aaaaa"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass
        })

        # HTTP 302 -> Redirect (Found)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.get("location"), "/story/login/")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertNotEqual(new_user, None)
        self.assertEqual(new_user.username, inp_name)
        self.assertEqual(new_user.display_name, inp_name)
        self.assertNotEqual(new_user.password, inp_pass)
        self.assertEqual(new_user.password, sha512(inp_pass.encode("utf-8")).hexdigest())

        return

    def test_bad_username(self) -> None:
        """
        Enter an invalid username (too short, too long, or bad chars) into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indicating "Invalid username."
        User should not in the db.
        """
        inp_name: str = "Yo"
        inp_pass: str = "!1Aaaaa"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Invalid username.")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertEqual(new_user, None)

        return

    def test_dup_username(self) -> None:
        """
        Enter a username that is already reserved into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indicating "Username is already taken."
        User should not be in the db.
        """
        orig_name: str = "Squidward"
        password: str = "!1Aaaaa"
        orig_dname: str = "uhhhhhhhh"

        # create an existing user in the database
        existing_user: User = User.objects.create(
            username=orig_name,
            password=password,
            display_name=orig_dname
        )

        new_dname: str = "different"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": orig_name,
            "password": password,
            "display_name": new_dname
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Username is already taken.")

        old_user: User = User.objects.get(username=orig_name)
        new_user: User = None
        try: new_user = User.objects.get(display_name=new_dname)
        except: pass

        self.assertEqual(old_user.display_name, orig_dname)
        self.assertEqual(new_user, None)

        return

    def test_bad_display_name(self) -> None:
        """
        Enter an invalid display name (too short, too long) into the field.
        Should redirect to the same page (/story/register/).
        A message should be present indiciating "Invalid display name."
        User should not be in the db.
        """
        inp_name: str = "Patrick"
        inp_pass: str = "!1Aaaaa"
        inp_dname: str = "jj"
        res: HttpResponse = self.client.post("/story/register/", data={
            "username": inp_name,
            "password": inp_pass,
            "display_name": inp_dname
        })

        # we aren't redirecting in this case, so we want a 200 status code
        # this indicates we're on the same page
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.has_header("location"), False)
        self.assertContains(res, "Invalid display name.")

        new_user: User = None
        try: new_user = User.objects.get(username=inp_name)
        except: pass

        self.assertEqual(new_user, None)

        return
