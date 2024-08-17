import unittest
import typewise_alert
from unittest.mock import patch


class TypewiseTest(unittest.TestCase):    
  def test_infers_breach_as_per_limits(self):
    self.assertTrue(typewise_alert.infer_breach(20, 50, 100) == 'TOO_LOW')
    self.assertTrue(typewise_alert.infer_breach(50, 50, 100) == 'NORMAL')
    self.assertTrue(typewise_alert.infer_breach(100, 50, 100) == 'NORMAL')
    self.assertTrue(typewise_alert.infer_breach(150, 50, 100) == 'TOO_HIGH')
  def test_infers_breach_based_on_cooling(self):
    self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 35) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', -5) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach('PASSIVE_COOLING', 36) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 45) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', -1) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach('HI_ACTIVE_COOLING', 46) == 'TOO_HIGH')
    self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 40) == 'NORMAL')
    self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', -2) == 'TOO_LOW')
    self.assertTrue(typewise_alert.classify_temperature_breach('MED_ACTIVE_COOLING', 41) == 'TOO_HIGH')
  @patch('builtins.print')
  def test_infers_breach_and_sends_confirmation(self,print_mock):
    typewise_alert.check_and_alert('TO_CONTROLLER', {'coolingType':'PASSIVE_COOLING'}, 35)
    print_mock.assert_called_with('65261, NORMAL')
    typewise_alert.check_and_alert('TO_EMAIL', {'coolingType':'PASSIVE_COOLING'}, 35)
    print_mock.assert_called_with('Hi, the temperature is normal')
    typewise_alert.send_to_controller('TOO_HIGH')
    print_mock.assert_called_with('65261, TOO_HIGH')
    typewise_alert.send_to_email('TOO_LOW')
    print_mock.assert_called_with('Hi, the temperature is too low')
    self.assertTrue(typewise_alert.check_and_alert('MED_ACTIVE_COOLING', {'coolingType':'PASSIVE_COOLING'},41) == 404)
    

if __name__ == '__main__':
  unittest.main()
