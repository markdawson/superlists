from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Jono is visiting our website for the first time.
        # He checks out the homepage first.
        self.browser.get(self.live_server_url)

        # He sees that the page title and header talk about to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),
                         'Enter a to-do item'
                         )

        # He types "Buy peacock feathers" into a test box
        # Jono's favorite hobby is tying fly-fish lures)
        inputbox.send_keys('Buy peacock feathers')

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list table
        inputbox.send_keys(Keys.ENTER)
        jono_list_url = self.browser.current_url
        self.assertRegex(jono_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a text box inviting him to add another item.
        # He enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now a new user, Francis comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of Jono's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Andy visits the home page. There is no sign of Jono's
        # list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Andy starts a new list by entering a new item. He
        # is less interesting than Jono. . .
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Andy gets his own unique URL
        andy_list_url = self.browser.current_url
        self.assertRegex(andy_list_url, '/lists/.+')
        self.assertNotEqual(andy_list_url, jono_list_url)

        # Again, there is no trace of Jono's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Buy milk', page_text)

        # Satisfied they both go back to sleep

        self.fail('Finish the test')

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep