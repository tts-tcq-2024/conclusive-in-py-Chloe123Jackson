cooling_type=['PASSIVE_COOLING', 'HI_ACTIVE_COOLING','MED_ACTIVE_COOLING']
temperature_breach_limits=[[0,35],[0,45],[0,40]]
BreachType_email_msg={'TOO_LOW': 'too low','TOO_HIGH': 'too high', 'NORMAL': 'normal'}
alertTargets=['TO_CONTROLLER','TO_EMAIL']


def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
  lowerLimit = 0
  upperLimit = 0
  try:
    if coolingType in cooling_type:
      statement_index=cooling_type.index(coolingType)
    else:
      raise OtherCoolingTypeNotAllowed
  except:
    print("Only cooling types PASSIVE_COOLING, MID_ACTIVE_COOLING and HI_ACTIVE_COOLING are allowed")
  lowerLimit=temperature_breach_limits[statement_index][0]
  upperLimit=temperature_breach_limits[statement_index][1]
  return infer_breach(temperatureInC, lowerLimit, upperLimit)


def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType =classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  try:
    if alertTarget in alertTargets:
        send_to_controller_or_email(breachType,alertTargets.index(alertTarget)
    else:
      raise AlertTargetOtherNotAllowed    
  except AlertTargetOtherNotAllowed:
    print("Please provide alertTarget as TO_CONTROLLER or TO_EMAIL")

def send_to_controller_or_email(breachType,recepient_index):
  header = 0xfeed
  recepient = "a.b@c.com"
  if recepient_index == 0:
    print(f'{header}, {breachType}')
  if recepient_index == 1:
    print(f'To: {recepient}')
    print(f'Hi, the temperature is {BreachType_email_msg[breachType]}')

  
class AlertTargetOtherNotAllowed(Exception):
  "Raised when alertTarget is set to a value other than TO_CONTROLLER or TO_EMAIL"
  pass
class OtherCoolingTypeNotAllowed(Exception):
  "Raised when a cooling Type apart from PASSIVE_COOLING, MID_ACTIVE_COOLING,HI_ACTIVE_COOLING is used in input"
  pass
