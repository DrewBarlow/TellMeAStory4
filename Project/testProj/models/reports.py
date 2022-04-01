from django.db import models



class Report(models.Model):
    #the id of the user who put in the report
    reporting_id = models.CharField(max_length=36, primary_key=True)

    #the id of the user who was reported
    reported_id = models.CharField(max_length=36)

    #the reason the user was reported (text field)
    report_reason = models.CharField(max_length=400)

    #makes the display in the DB the reporting_id
    def __str__(self):
        return self.reporting_id

    # accessor methods
    def get_reporting_id(self):
        return self.reporting_id

    def get_reported_id(self):
        return self.reported_id

    def get_report_reason(self):
        return self.report_reason