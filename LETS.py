from dataclasses import asdict
import json
from re import A
import requests
import random  
import string
import matplotlib.pyplot as plt
import time
import numpy as np, numpy.random
import db
import socket

# Connect Database
c_con, c_curs = db.connect_db()
headers = {
  'Accept': 'application/json',
  'Authorization': 'Token r7drn3dYBB+m4y6GQcVIWv8dO2A0U+0S'
}

timearr = []
timearr2 = []
runs = []
cou = 0

# Zeitmessung der Barcodegenerierung
def measure_time(x):
  global cou
  
  if x:
    global start
    start = time.perf_counter()
  else:
    cou = cou + 1
    end = time.perf_counter() - start
    if (cou % 2) == 0:
      timearr.append(end * 10000)
    else:
      timearr2.append(end * 10000)

# Wichtige Daten für Mitarbeitertests werden aus der "Dyflexis"-API extrahiert
def map_serial_to_emp_number(card_number):
  barcode_taken = True

  while barcode_taken:
    barcode = construct_barcode(8)
    c_curs.execute("SELECT * FROM barcodes WHERE barcode='{}'".format(barcode))
    if c_curs.fetchone() is None:
      c_curs.execute("INSERT INTO barcodes(barcode) VALUES ('{}')".format(barcode))
      c_con.commit()
      barcode_taken = False

  card_number = str(card_number).lower()
  print(card_number)
  counter = 1
  employeeData = ''
  while employeeData != '[]':
    r = requests.get('https://app.planning.nu/lifebrain/api2/employee-data?page={}'.format(counter), headers = headers)
    employeeData = r.json()["employeeData"]


    for i in employeeData:
      if str(i['cardNumbers']) == card_number:
        print(i['firstName'])

        empNr = str(i['partnerLastNamePrefix'])[-4:]
        SVNr = str(i['partnerLastNamePrefix'])[:-5]
        dateOfBirth = str(i['partnerLastNamePrefix'])[4:-5]
        dyflexisid = str(i['dyflexisId'])
        firstName = str(i['firstName'])
        lastName = str(i['lastName'])

        c_curs.execute("SELECT DATE_FORMAT(gebdat, '%Y-%m-%d') FROM gebdats WHERE dyfid='{}'".format(dyflexisid))

        json_data = ('''
        {{"sender_id": "Lifebrain",
        "firstName": "{}",
        "lastName": "{}",
        "email": "{}",
        "SVNr": "{}",
        "EmpNr": "{}",
        "date_of_birth": "{}",
        "barcode": "{}"}}
        ''').format(firstName, lastName, i['email'], SVNr, empNr, str(c_curs.fetchone()[0]), barcode)

    employeeData = str(employeeData)

    if employeeData != '[]':
      counter += 1

# Daten werden an Drucker gesendet, Drucker druckt Barcode mit Mitarbeiternamen
  if 'json_data' in locals():
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)         
    host = "10.90.1.126" 
    port = 9100   
    name = lastName.encode('utf-8')
    firstName = firstName.encode('utf-8')
    ebarcode = barcode.encode('utf-8')
    label = 'Lifebrain Employee Testing Service'.encode('utf-8')
    try:           
      mysocket.connect((host, port)) #connecting to host
      mysocket.send(b'^XA'
      b'^CI28'
      b'^LH00,15'
      b'^BY2,3,50'
      b'^FO33,0^BCN,80,N,Y,N^FD' + ebarcode + b'^FS'
      b'^FO85,90^A0N,30,35^FD' + ebarcode + b'^FS'
      b'^FO30,125^A0N,20,35^FD' + name + b', ' + firstName + b'^FS'
      b'^FO30,150^A0N,18,24^FD' + label + b'^FS'
      b'^XZ')
      mysocket.close () #closing connection
    except:
      print("Error with the connection")
    return json_data
  else:
    return 'Card may not exist in our system or the list is corrupt.'

def printjson():
  counter = 1
  employeeData = ''
  while employeeData != '[]':
    r = requests.get('https://app.planning.nu/lifebrain/api2/employee-data?page={}'.format(counter), headers = headers)

    employeeData = r.json()["employeeData"]
    print(employeeData)

    employeeData = str(employeeData)
    if employeeData != '[]':
      counter += 1

# Visualisierungsfunktion (Spielerei)
def plot_gaussian(iters):
  sample_string = 'ABCDEFGHIJKLMNOPQRSTUVWX0123456789'
  prefix = 'EMPS'
  arr = []
  arr2 = []
  arr3 = []
  arr4 = []

  for j in range(iters):
    barcode = prefix + ''.join((random.choice(sample_string)) for x in range(8))
    val = 0
    for i in range(len(barcode)):
      val = val + ord(barcode[i])
    arr.append(val)
    arr2.append(barcode)

  for k in range(693,1013):
    arr = np.array(arr)
    test = np.where(arr==k)
    test2 = np.array(test).size
    arr3.append(k)
    arr4.append(test2)

  fig = plt.figure()
  
  plt.bar(arr3,arr4)
  plt.xlabel('Quersumme')
  plt.ylabel('Auftreten')
  plt.show()

  def minimum():
    mi = max(arr)
    lowest = arr2[arr.index(mi)] 
    sum = 0
    for k in range(len(arr)):
      sum = sum + arr[k] 
    avg = sum / len(arr)    
    return avg, lowest

# Verschiedene Attempts, Barcodes zu generieren

## ATTEMPT 1 ##
def generate_barcode():
  
  sample_string = 'ABCDEFGHIJKLMNOPQRSTUVWX0123456789'
  prefix = 'EMPS'
  val = 0
  counter = 0

  while val != 860:
      counter += 1
      bar_code = ''
      bar_code = prefix + ''.join((random.choice(sample_string)) for x in range(8))
      val = 0
      for i in range(len(bar_code)):
        val = val + ord(bar_code[i])
  
  return val, bar_code

## ATTEMPT 2 ##
def construct_barcode(length):
  
  map_chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
  max_val = 33
  amount_of_v = max_val + 1
  avg_val_sum = length * (max_val / 2)

  arr = np.random.dirichlet(np.ones(length), size=1)
  arr = arr.flatten() * avg_val_sum
  
  while max(arr) > max_val:
    for i in range(len(arr)):
      if arr[i] > max_val:
        res = (length-1) / length * arr[i]
        arr[i] = 1 / length * arr[i]
        for j in range(len(arr)):
          ap = res / length
          arr[j] = arr[j] + ap

  arr = np.around(arr)

  if sum(arr) != avg_val_sum:
    delta = avg_val_sum - sum(arr)
    for i in range(len(arr)):
      if delta + arr[i] < amount_of_v:
        arr[i] = arr[i] + delta 
        delta = 0
        
  string = ''
  for i in range(len(arr)):
    string = string + map_chars[int(arr[i])]
  
  return 'EMPS' + string

# Visualisierungsfunktion für Laufzeit (Spielerei)
def plot_time(iters):
  for i in range(iters):
    (construct_barcode(8))
    (generate_barcode())

  sr_cons = 0
  sr_sear = 0

  for i in range(len(timearr)):
    if timearr[i] < timearr2[i]:
      sr_sear += 1
    else:
      sr_cons += 1

  x = list(range(0, iters))
  plt.plot(x, timearr, label = "Runtime of searching for barcode")
  plt.plot(x, timearr2, label = "Runtime of constructing barcode")
  plt.xlabel('Iterations')
  plt.ylabel('microseconds')
  plt.suptitle('Runtime comparison, in µs', fontsize=20)
  plt.title('Constructing barcode was faster {} times. \n Searching for barcode was faster {} times.'.format(sr_cons, sr_sear), fontsize=12)
  plt.legend()
  plt.show()
  


# Ablauf

# GUI, Karte hinhalten? WebApp?
# Send JSON to Orchestra

# wait (async?)

# get Response: Successful Y/N?

# If Yes

# check if barcode unique?

# If Yes
# Print Barcode
