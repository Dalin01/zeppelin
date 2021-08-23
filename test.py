import unittest
import api_service
import json
from model.index import format_data

class TestGETRequest(unittest.TestCase):

  def testGetRequest(self):
    res = json.loads(api_service.api_service().content)
    if 'success' in res:
      self.assertTrue(res['success'])
    else:
      self.assertEqual(res['error']['code'], 'invalid_access_key')

class TestFormatData(unittest.TestCase):
  
  def testFormating(self):
    res = json.loads(api_service.api_service().content)
    response = format_data(res)
    self.assertTrue(isinstance(response, dict))
    self.assertTrue(isinstance(response['payload'], list))
    self.assertTrue(len(response['payload'][0]) > 0)
    
if __name__ == '__main__':
    unittest.main()