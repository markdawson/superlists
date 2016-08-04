from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Jono is visiting our website for the first time.
		# He checks out the homepage first.
		self.browser.get('http://localhost:8000')

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
		inputbox.send_keys(Keys.Enter)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Buy peacock feathers' for row in rows)
		)

		# There is stilll a text box inviting him to add another item.
		# He enters "Use peacock feathers to make a fly"
		self.fail('Finish the test')

if __name__ == '__main__':
	unittest.main(warnings='ignore')
