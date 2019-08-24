from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

# https://medium.com/django-musings/integration-testing-on-django-1ac6a0c428c8

class InsightMatrixFunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(InsightMatrixFunctionalTests, cls).setUpClass()
        cls.selenium = webdriver.Chrome()

    def test_user_signs_up_for_an_account(self):
        """When a user first goes to the site, they should see a short
        description of what it is. They should be able to sign up for an
        account and log in.
        """
        # A user visits the site homepage.
        self.selenium.get('{}/'.format(self.live_server_url))

        self.assertTrue("Insight Matrix is a tool for finding patterns" in self.selenium.page_source)

        # Find the login button.
        self.selenium.find_element_by_link_text("Login to your account").click()

        # Try to login.
        # But it fails.

        # Back to the homepage.
        #self.selenium.get('{}/'.format(self.live_server_url))

        # Find the login button.
        #self.selenium.find_element_by_link_text("sign up for a new account")

        # Sign up for an account.
        # Now try logging in.
        # It succeeds.
        # They should land on the project list page, which will be empty.

    '''
    def test_user_creates_first_project(self):
        """Log in. go to project list page. it should be empty.
        Follow link to create a new project. just add name and description. Save.
        Go to project list page. It should be there.
        Edit the project. Add some labels. Save it.
        Labels should appear somewhere.
        Remove a label. 
        That labels should be gone now.
        """
        raise NotImplementedError

    def test_user_creates_similarity_pairs(self):
        """Create a new project with some labels.
        Click the link to enter pairwise comparisons.
        There should be so many comparisons for so many labels. Keep track as
        you go to be sure it's the right number.
        enter 0-2 in some pattern. 
        when they're all filled out you should go to a different view. 
        """
        raise NotImplementedError
    
    def test_users_who_arent_logged_in_get_redirected(self):
        """A repeat visitor might have a URL saved in their browser that
           requires them to be logged in. Be sure all of those urls correctly
           redirect users who aren't logged in to the login page.
           /project/create/
           /project/list/
           /project/update/1/
           /similarity/1/
           /similarity/list/1/
        """
        raise NotImplementedError
    '''
