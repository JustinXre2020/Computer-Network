import os
from datetime import datetime
import time

userinfo = 'chat-history.txt'
userinfo_path = os.path.join(os.getcwd(), userinfo)         # generate userinfo path
mode = 'r+' if os.path.exists(userinfo_path) else 'a'      # set mode (append & read or write & read) 
                                                            # based on the existance of userinfo
msg = "Howdy world!"

with open(userinfo_path, mode) as f:
    # write the file
    for i in range(10):
        f.write(f"At {datetime.now()}, BM, Run sends John: {msg}\n")
        # f.write("Justin Xiao \n")
       

with open(userinfo_path, mode) as f:
    lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
    # nested_list = [line.strip().split(',') for line in lines]
    # data_list = [data for list in nested_list for data in list]
    for i in lines:
        print(i)


# l = ['123', '456', '789']
# ss = " ".join(l)

# m = {"john" : "ss"}
# m.update({"john" : "ss"})
# m.update({"john" : "mm"})
# m.update({'run' : 'ss'})
# ll = {item[0] : item[1] for item in m.items() if item[0] != 'run'}
# print(ll)

# l = "Howdy welcome back!"
# ll = l.encode()

# try:
#     data = l.decode()
#     print(data)
# except (UnicodeDecodeError, AttributeError):
#     print(l)

# from pg3lib import *

# # key = getPubKey()

# # print(key.decode())

# # key_server = b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6TXZuLzRDbjNpZis4NzBPUHpQdAo4NVFGRkRvajdpelc3OG1OUElLWWE2WFdFZ2pTK1JNSjVMcTZIYUFielFtclJIeXQ2a2JMQWJPVmY1WWhMRGo1CmNaYzh2RXhuZ1lJTnpIcmlOMEpSa1hJaEp0Nk03ZDBqeXRlR3ZPeHE3eGFEcU5nbC90QlZ0VWNLZWM3Z3BGVlIKWk56djZDcWh1NVc4R2p0OFRNcTF4Mm85dkxIV29UR1R6bmlBSTZMd3lHd0JHTmdLbHRjaCtXa0RvMjZoVk4wdQpHcFRrUkVNQjMrczBJS1ZoazYyQVViR1ZNNU53cFVWTVJPcFNRUHlhRkpKUXdvajJPcFdIemxyTzE5VE1BUnhRCitLTkVTWExQaEZoTURvTk5BQ2QyMFZPb0ZRTUpJcjFyVHU4RVpRZGFxT1ducThQOWVmNHgzVnJGM0ZGMUFKSUQKWHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=='

# key_client = b'LS0tLS1CRUdJTiBQVUJMSUMgS0VZLS0tLS0KTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6TXZuLzRDbjNpZis4NzBPUHpQdAo4NVFGRkRvajdpelc3OG1OUElLWWE2WFdFZ2pTK1JNSjVMcTZIYUFielFtclJIeXQ2a2JMQWJPVmY1WWhMRGo1CmNaYzh2RXhuZ1lJTnpIcmlOMEpSa1hJaEp0Nk03ZDBqeXRlR3ZPeHE3eGFEcU5nbC90QlZ0VWNLZWM3Z3BGVlIKWk56djZDcWh1NVc4R2p0OFRNcTF4Mm85dkxIV29UR1R6bmlBSTZMd3lHd0JHTmdLbHRjaCtXa0RvMjZoVk4wdQpHcFRrUkVNQjMrczBJS1ZoazYyQVViR1ZNNU53cFVWTVJPcFNRUHlhRkpKUXdvajJPcFdIemxyTzE5VE1BUnhRCitLTkVTWExQaEZoTURvTk5BQ2QyMFZPb0ZRTUpJcjFyVHU4RVpRZGFxT1ducThQOWVmNHgzVnJGM0ZGMUFKSUQKWHdJREFRQUIKLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tCg=='

# encrypt("Howdy world!".encode(), key_client)
