from django.test import TestCase
from ..models import Post,UserTable,Report


class testPost(TestCase):
    #testing Post database functionality
    def test_get_retrieval_post(self):
        # create some objects
        Post.objects.create(user_id="IAJDIAWKFAO", post_id="DWADAWDAD", postText="My first post!")
        Post.objects.create(user_id="AWDAWASFAW", post_id="26q2aa263a2", postText="My second post!")

        # get by the post_id (primary key)
        first_post = Post.objects.get(post_id = "DWADAWDAD")
        second_post = Post.objects.get(post_id="26q2aa263a2")

        #check if the text is equal in the database
        self.assertEqual(first_post.postText, "My first post!")
        self.assertEqual(second_post.postText, "My second post!")

    #testing UserTable database functionality
    def test_get_retrieval_user(self):
        #create some objects
        UserTable.objects.create(user_id="IAJDIAWKFAO", name = "Joe Bob", email="bob@gmail.com", username="jo1249", password="qwertyuiop")
        UserTable.objects.create(user_id="AWDAWASFAW",  name = "Kyle Joseph", email="Joseph@gmail.com", username="john42885", password="oagkawdoa")

        #get by the user_id (primary key)
        first_post = UserTable.objects.get(user_id = "IAJDIAWKFAO")
        second_post = UserTable.objects.get(user_id="AWDAWASFAW")

        #check if the passwords are equal
        self.assertEqual(first_post.password, "qwertyuiop")
        self.assertEqual(second_post.password, "oagkawdoa")

    #testing UserTable database functionality
    def test_get_retrieval_report(self):
        #create some objects
        Report.objects.create(reporting_id="IAJDIAWKFAO", reported_id = "Jawgawfawfa", report_reason="Bullying")
        Report.objects.create(reporting_id="awdawda262", reported_id = "awdaawdagw", report_reason="Harrasment")

        #get by the reporting_id (primary key)
        first_post = Report.objects.get(reporting_id = "IAJDIAWKFAO")
        second_post = Report.objects.get(reporting_id="awdawda262")

        #check if the passwords are equal
        self.assertEqual(first_post.report_reason, "Bullying")
        self.assertEqual(second_post.report_reason, "Harrasment")
