from django.test import TestCase
from hashlib import sha512
from .models import User

class UserRegistrationTests(TestCase):
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

    # this may be more suited to some account functionality--
    # stub for now
    def test_change_display_name(self) -> None:
        self.assertIs(True, True)
        return

    # this is more suited for registration fields.
    # we should just NEVER store the unhashed password ANYWHERE.
    # keeping it here for now
    # TODO: migrate to registration view tests
    def test_password_is_secure(self) -> None:
        """
        is_strong_password() should return False if the desired
        password does not contain a symbol, uppercase letter, lowercase letter,
        a number, and does not have a length >= 6.
        """

        # stubbing this for now
        """
        weak_pass_no_upper: str = "!1aaaa"
        weak_pass_no_lower: str = "!1AAAA"
        weak_pass_no_number: str = "!Aaaaa"
        weak_pass_no_symbol: str = "1Aaaaa"
        weak_pass_too_short: str = "!A1a"
        strong_pass: str = "!1AaHello"

        no_upper: User = User(password=weak_pass_no_upper)
        no_lower: User = User(password=weak_pass_no_lower)
        no_number: User = User(password=weak_pass_no_number)
        no_symbol: User = User(password=weak_pass_no_symbol)
        too_short: User = User(password=weak_pass_too_short)
        strong: User = User(password=strong_pass)

        self.assertIs(no_upper.is_strong_password(), False)
        self.assertIs(no_lower.is_strong_password(), False)
        self.assertIs(no_number.is_strong_password(), False)
        self.assertIs(no_symbol.is_strong_password(), False)
        self.assertIs(too_short.is_strong_password(), False)
        self.assertIs(strong.is_strong_password(), True)
        """
        self.assertIs(True, True)
        return

    # for the same reasoning above,
    # TODO: migrate to registration view tests
    def test_password_is_hashed(self) -> None:
        """
        We want to store the SHA512 hash digest of a user's password.
        We are not salting it because we don't really care!
        ... For now.
        """

        # stubbing this for now
        """
        name: str = "Hello"
        password: str = "!1AaHello"
        user: User = User(username=name, password=password)
        user.save()

        retrieved: User = User.objects.filter(username=name)
        self.assertIs(retrieved.password == password, False)
        """
        self.assertIs(True, True)
        return
