temperature_breach_stmt=['PASSIVE_COOLING', 'HI_ACTIVE_COOLING','MED_ACTIVE_COOLING']
temperature_breach_limits=[[0,35],[0,45],[0,40]]
BreachType_email_msg={'TOO_LOW': 'is too low','TOO_HIGH': 'is too high'}
alertTarget_dict={'TO_CONTROLLER': 'TO_EMAIL'}

def infer_breach(value, lowerLimit, upperLimit):
  if value < lowerLimit:
    return 'TOO_LOW'
  if value > upperLimit:
    return 'TOO_HIGH'
  return 'NORMAL'


def classify_temperature_breach(coolingType, temperatureInC):
  lowerLimit = 0
  upperLimit = 0
  statement_index=temperature_breach_stmt.index(coolingType)
  lowerlimit=temperature_breach_limits[statement_index][0]
  upperlimit=temperature_breach_limits[statement_index][1]
  return infer_breach(temperatureInC, lowerLimit, upperLimit)


def check_and_alert(alertTarget, batteryChar, temperatureInC):
  breachType =classify_temperature_breach(batteryChar['coolingType'], temperatureInC)
  if alertTarget == 'TO_CONTROLLER':
    send_to_controller(breachType)
  elif alertTarget == 'TO_EMAIL':
    send_to_email(breachType)


def send_to_controller(breachType):
  header = 0xfeed
  print_breachtype(header,breachType,0)


def send_to_email(breachType):
  recepient = "a.b@c.com"
  print_breachtype(recepient, breachType,1)
  
  
def print_breachtype(header_or_recepient, breachType,controller_or_email):
  if controller_or_email == 0:
    print(f'{header_or_recepient}, {breachType}')
  if controller_or_email == 1:
    print(f'To: {header_or_recepient}')
    print(f'Hi, the temperature is {BreachType_email_msg[breachType]}')
