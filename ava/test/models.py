from django.db import models
from django.contrib.auth.models import User

from ava.core.models import TimeStampedModel, ReferenceModel
from ava.core_project.models import Project


class Test(ReferenceModel):
    EMAIL = 'EMAIL'
    TWITTER = 'TWITTER'

    TEST_TYPE_CHOICES = (
        (EMAIL, 'Email'),
        (TWITTER, 'Twitter'),
    )

    TEST_TYPE_ICONS = (
        (EMAIL, 'envelope'),
        (TWITTER, 'twitter'),
    )

    NEW = 'NEW'
    COMPLETE = 'COMPLETE'
    ERROR = 'ERROR'
    SCHEDULED = 'SCHEDULED'
    RUNNING = 'RUNNING'

    TEST_STATUS_CHOICES = (
        (NEW, 'New'),
        (COMPLETE, 'Complete'),
        (ERROR, 'An error occurred'),
        (SCHEDULED, 'Scheduled'),
        (RUNNING, 'In progress'),
    )

    # The project that the test is tied to.
    project = models.ForeignKey(Project, related_name='tests', null=True)
    # (OBSOLETE) The user who owns the test.
    user = models.ForeignKey(User, null=True)

    # The type of test being performed.
    test_type = models.CharField(max_length=7,
                                 choices=TEST_TYPE_CHOICES,
                                 default=EMAIL,
                                 verbose_name='Test Type')
    # The current status of the test.
    test_status = models.CharField(max_length=10,
                                   choices=TEST_STATUS_CHOICES,
                                   default=NEW,
                                   verbose_name='Test Status')

    # Optional URL that users are redirected to after clicking on the link.
    redirect_url = models.CharField(max_length=2000, null=True, blank=True)
    # Optional page template to display after clicking on the link. Not used
    # if a redirect URL is specified.
    page_template = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name or ''


class TestResult(TimeStampedModel):

    class Meta:
        abstract = True

    ip_address = models.CharField(max_length=50)
    method = models.CharField(max_length=10)  # GET/POST/etc
    host = models.CharField(max_length=260)  # host name:port
    path = models.TextField(null=True, blank=True)  # /path/to/page/
    content_length = models.CharField(max_length=10, null=True, blank=True)
    content_type = models.CharField(max_length=100, null=True, blank=True)
    ua = models.TextField(null=True, blank=True)  # User-Agent
    referrer = models.TextField(null=True, blank=True)  # Referer
    via = models.TextField(null=True, blank=True)  # Via

    def __str__(self):
        return str(self.created)
