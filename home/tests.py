from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import time

class InsightMatrixFunctionalTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(InsightMatrixFunctionalTests, cls).setUpClass()
        cls.selenium = webdriver.Safari()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

    def test_user_signs_up_for_an_account(self):
        """When a user first goes to the site, they should see a short
        description of what it is. They should be able to sign up for an
        account and log in.
        """
        # A user visits the site homepage.
        self.selenium.get('{}/'.format(self.live_server_url))

        # They see some helpful text telling them what this site is about.
        self.assertTrue("Insight Matrix is a tool for finding patterns" in self.selenium.page_source)

        # They find the login button.
        self.selenium.find_element_by_link_text("Login to your account").click()
        time.sleep(1)

        # This user doesn't have an account, but tries to log in.
        self.selenium.find_element_by_id("id_username").send_keys("nobody")
        self.selenium.find_element_by_id("id_password").send_keys("nopassword")
        self.selenium.find_element_by_tag_name("form").submit()
        time.sleep(1)

        # They get a message saying that their password is incorrect.
        self.assertTrue("Please enter a correct username and password." in self.selenium.page_source)

        # Back to the homepage.
        self.selenium.get('{}/'.format(self.live_server_url))
        time.sleep(1)

        # Now the user clicks to sign up for a new account.
        self.selenium.find_element_by_link_text("sign up for a new account").click()
        time.sleep(1)

        # The user fills out our form.
        self.selenium.find_element_by_id("id_username").send_keys("somebody")
        self.selenium.find_element_by_id("id_password1").send_keys("somebodyspassword")
        self.selenium.find_element_by_id("id_password2").send_keys("somebodyspassword")
        self.selenium.find_element_by_tag_name("form").submit()
        time.sleep(1)

        # Now try logging in.
        self.selenium.find_element_by_id("id_username").send_keys("somebody")
        self.selenium.find_element_by_id("id_password").send_keys("somebodyspassword")
        self.selenium.find_element_by_tag_name("form").submit()
        time.sleep(1)

        # It succeeds. They get redirected to an empty project page.
        self.assertTrue("There are currently no projects." in self.selenium.page_source)

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
