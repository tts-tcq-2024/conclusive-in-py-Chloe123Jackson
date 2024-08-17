temperature_breach_stmt=['PASSIVE_COOLING', 'HI_ACTIVE_COOLING','MED_ACTIVE_COOLING']
temperature_breach_limits=[[0,35],[0,45],[0,40]]
BreachType_email_msg={'TOO_LOW': 'too low','TOO_HIGH': 'too high', 'NORMAL': 'normal'}


def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
  lowerLimit = 0
  upperLimit = 0
  statement_index=temperature_breach_stmt.index(coolingType) # exception required
  lowerLimit=temperature_breach_limits[statement_index][0]
  upperLimit=temperature_breach_limits[statement_index][1]
  return infer_breach(temperatureInC, lowerLimit, upperLimit)


def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType =classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  try:
    if alertTarget == 'TO_CONTROLLER':
      send_to_controller(breachType)
    elif alertTarget == 'TO_EMAIL':
      send_to_email(breachType)
  except AlertTargetOtherNotAllowed:
    print("Please provide alertTarget as TO_CONTROLLER or TO_EMAIL")
    return 404

def send_to_controller(breachType):
  header = 0xfeed
  print(f'{header}, {breachType}')


def send_to_email(breachType):
  recepient = "a.b@c.com"
  print(f'To: {recepient}')
  print(f'Hi, the temperature is {BreachType_email_msg[breachType]}')
  
class AlertTargetOtherNotAllowed(Exception):
  "Raised when alertTarget is set to a value other than TO_CONTROLLER or TO_EMAIL"
  pass
