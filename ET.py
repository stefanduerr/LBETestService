# import usb.core
# import sys
# # idVendor="0x09d8", idProduct="0x0410"

# # dev = usb.core.find(find_all=True)

# # for cfg in dev:
# #     sys.stdout.write('Hexadecimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n\n')
# #     print(cfg.idVendor)

# # import hid

# # for device_dict in hid.enumerate():
# #     keys = list(device_dict.keys())
# #     keys.sort()
# #     for key in keys:
# #         print("%s : %s" % (key, device_dict[key]))
# #     print()
    

# dev2 = usb.core.find(idVendor=2520, idProduct=1040)



# dev2.reset()

# print(dev2[0].interfaces()[0].endpoints()[0])
# ep=dev2[0].interfaces()[0].endpoints()[0]
# i=dev2[0].interfaces()[0].bInterfaceNumber
# # assert ep is not None
# # 
# print(ep.bEndpointAddress)
# dev2.set_configuration()
# dev2.read(ep.bEndpointAddress, ep.wMaxPacketSize)



# if dev2.is_kernel_driver_active(i):
#     dev2.detach_kernel_driver(i)

# dev2.set_configuration()
# eaddr=ep.bEndpointAddress

# r=dev2.read(eaddr, 1024)
# print(len(r))
# dev2.set_configuration()

# # get an endpoint instance
# cfg = dev2.get_active_configuration()
# intf = cfg[(0,0)]
# # print(dev)
# ep = usb.util.find_descriptor(
#     intf,
#     # match the first OUT endpoint
#     custom_match = \
#     lambda e: \
#         usb.util.endpoint_direction(e.bEndpointAddress) == \
#         usb.util.ENDPOINT_OUT)

# 

# write the data
# ep.write('test')
# ep=dev[0].interfaces()[0].endpoints()[0]
# i=dev[0].interfaces()[0].bInterfaceNumber
# dev.reset()

# if dev.is_kernel_driver_active(i):
#     dev.detach_kernel_driver(i)
import numpy as np
import time
# dev.set_configuration()
# eaddr=ep.bEndpointAddress

# r=dev.read(eaddr,1024)
def random_gen2():
  
  length = 8
  amount_of_v = 34
  max_val = amount_of_v - 1
  avg_val_sum = length * max_val


  arr = np.random.dirichlet(np.ones(8), size=1)
  arr = arr.flatten() * 132
  # #print(arr, sum(arr))
  
  while max(arr) > 33:
    for i in range(len(arr)):
      if arr[i] > 33:
        res = 7 / 8 * arr[i]
        arr[i] = 1 / 8 * arr[i]
        for j in range(len(arr)):
          ap = res / 8
          arr[j] = arr[j] + ap
  #print(arr, sum(arr))
  arr = np.around(arr)
  #print(arr, sum(arr))
  if sum(arr) != 132:
    delta = 132 - sum(arr)
    for i in range(len(arr)):
      if delta + arr[i] < 34:
        arr[i] = arr[i] + delta 
        delta = 0
  print(arr, sum(arr))

def random_gen(length, max_val):
  map_chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X']
  # length = 8
  # amount_of_v = 34
  amount_of_v = max_val + 1
  avg_val_sum = length * (max_val / 2)

  arr = np.random.dirichlet(np.ones(length), size=1)
  arr = arr.flatten() * avg_val_sum
  # #print(arr, sum(arr))
  
  while max(arr) > max_val:
    for i in range(len(arr)):
      if arr[i] > max_val:
        res = (length-1) / length * arr[i]
        arr[i] = 1 / length * arr[i]
        for j in range(len(arr)):
          ap = res / length
          arr[j] = arr[j] + ap

  #print(arr, sum(arr))
  arr = np.around(arr)
  #print(arr, sum(arr))

  if sum(arr) != avg_val_sum:
    delta = avg_val_sum - sum(arr)
    for i in range(len(arr)):
      if delta + arr[i] < amount_of_v:
        arr[i] = arr[i] + delta 
        delta = 0
        
  # print(arr, sum(arr))
  arr2 = []
  string = ''
  for i in range(len(arr)):
    string = string + map_chars[int(arr[i])]
  
  print(arr, 'EMPS', string, sum(arr))


while True:
  random_gen(8, 33)
  time.sleep(0.1)


#     sys.stdout.write('Hexadecimal VendorID=' + str(cfg.idVendor) + ' & ProductID=' + str(cfg.idProduct) + '\n\n')
def big_nrs():
  a_dictionary = [["Tsd.", 4],["Mil.", 7],["Bil.", 10],["Tril.", 13]]
  value = 1
  num = len(str(value))

  for j in range(20):
      value = j ** j
      num = len(str(value))
      for i in range(len(a_dictionary)):
          # print('unformatted: ' + str(value))
          if a_dictionary[i][1] <= num and num - a_dictionary[i][1] < 3:
              # print(str(num) + ' ' + str(a_dictionary[i][1]))
              frm = int('1' + (a_dictionary[i][1]-1) * '0')
              print(str(round(value/frm, 2)) + ' ' + str(a_dictionary[i][0]))


def faculty(f):
  a = 1
  for i in range(f+1):
    if i != 0:
      a = a * i
  return a

# print(faculty(20))