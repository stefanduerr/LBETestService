
import numpy as np
import time


# Generate random Barcodes in the desired format
def random_gen2():
  
  length = 8
  amount_of_v = 34
  max_val = amount_of_v - 1
  avg_val_sum = length * max_val


  arr = np.random.dirichlet(np.ones(8), size=1)
  arr = arr.flatten() * 132
  
  while max(arr) > 33:
    for i in range(len(arr)):
      if arr[i] > 33:
        res = 7 / 8 * arr[i]
        arr[i] = 1 / 8 * arr[i]
        for j in range(len(arr)):
          ap = res / 8
          arr[j] = arr[j] + ap
  arr = np.around(arr)
  if sum(arr) != 132:
    delta = 132 - sum(arr)
    for i in range(len(arr)):
      if delta + arr[i] < 34:
        arr[i] = arr[i] + delta 
        delta = 0
  print(arr, sum(arr))

# Generate random Barcodes in the desired format
def random_gen(length, max_val):
  map_chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
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
        
  arr2 = []
  string = ''
  for i in range(len(arr)):
    string = string + map_chars[int(arr[i])]
  
  print(arr, 'EMPS', string, sum(arr))

# For test purposes
while True:
  random_gen(8, 33)
  time.sleep(0.1)


def big_nrs():
  a_dictionary = [["Tsd.", 4],["Mil.", 7],["Bil.", 10],["Tril.", 13]]
  value = 1
  num = len(str(value))

  for j in range(20):
      value = j ** j
      num = len(str(value))
      for i in range(len(a_dictionary)):
          if a_dictionary[i][1] <= num and num - a_dictionary[i][1] < 3:
              frm = int('1' + (a_dictionary[i][1]-1) * '0')
              print(str(round(value/frm, 2)) + ' ' + str(a_dictionary[i][0]))


def faculty(f):
  a = 1
  for i in range(f+1):
    if i != 0:
      a = a * i
  return a
