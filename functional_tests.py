from selenium import webdriver
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
		self.fail('Finish the test!')

if __name__ == '__main__':
	unittest.main(warnings='ignore')