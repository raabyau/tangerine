from django.test import TestCase
from chatbot.chat import QuestionSet

# Unit tests for the QuestionSet class
class QuestionSetTestCase(TestCase):

	def test_single_question(self):
		p = {"q1": 
				{
					"text": "question1", 
					"response": { 
						"type": "str", 
						"conditions": {"min": {"val": 5, "errmsg": "error message"}}
					}
				}
			}
		q = {"first": "q1", 
			 "q1": "last"}

		qs = QuestionSet(p,q)

		# There should be questions remaining (1 to be exact)
		self.assertEqual(qs.remaining, True)

		_ = qs.next()
		qs.check("123456")

		# There shouldn't be any questions remaining
		self.assertEqual(qs.remaining, False)

	def test_string_minlen_constraint(self):
		p = {"q1": 
				{
					"text": "question1", 
					"response": { 
						"type": "str", 
						"conditions": {"min": {"val": 5, "errmsg": "string must be more than {} characters in length"}}
					}
				}
			}
		q = {"first": "q1", 
			 "q1": "last"}

		qs = QuestionSet(p,q)

		# string length of 4 is less than the minimum of 5.
		_ = qs.next()
		res = qs.check("1234")

		self.assertEqual(res["result"], False)

		# string length of 5 is the minimum
		res = qs.check("12345")
		self.assertEqual(res["result"], True)

		# string length of 6 is over the minimum
		qs.reset()
		prompt = qs.next()
		res = qs.check("123456")
		self.assertEqual(res["result"], True)

	def test_integer_maxlen_constraint(self):
		p = {"q1": 
				{
					"text": "question1", 
					"response": { 
						"type": "str", 
						"conditions": {"max": {"val": 5, "errmsg": "string must be more than {} characters in length"}}
					}
				}
			}
		q = {"first": "q1", 
			 "q1": "last"}

		qs = QuestionSet(p,q)

		# string length of 4 is less than the maximum of 5.
		_ = qs.next()
		res = qs.check("1234")

		self.assertEqual(res["result"], True)

		# string length of 5 is the maximum
		qs.reset()
		_ = qs.next()
		res = qs.check("12345")
		self.assertEqual(res["result"], True)

		# string length of 6 is over the maximum
		qs.reset()
		_ = qs.next()
		res = qs.check("123456")
		self.assertEqual(res["result"], False)

	def test_date_format_constraint(self):
		p = {"q1": 
				{
					"text": "question1", 
					"response": { 
						"type": "date",
						"errmsg": "invalid date",
					}
				}
			}
		q = {"first": "q1", 
			 "q1": "last"}

		qs = QuestionSet(p,q)

		# Invalid date
		_ = qs.next()
		res = qs.check("1999")
		self.assertEqual(res["result"], False)


		# Valid date
		res = qs.check("31-12-1999")
		self.assertEqual(res["result"], True)

