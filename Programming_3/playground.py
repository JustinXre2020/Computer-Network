# import os

# userinfo = 'userinfo.txt'
# userinfo_path = os.path.join(os.getcwd(), userinfo)         # generate userinfo path
# # mode = 'r+' if os.path.exists(userinfo_path) else 'w+'      # set mode (append & read or write & read) 
#                                                             # based on the existance of userinfo
# with open(userinfo_path, 'w') as f:
#     # write the file
#     for i in range(10):
#         f.write("Justin" + ',')
#         f.write("Xiao" + '\n')

# with open(userinfo_path, 'r') as f:
#     lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
#     # nested_list = [line.strip().split(',') for line in lines]
#     # data_list = [data for list in nested_list for data in list]
#     for i in lines:
#         print(i)


# l = ['123', '456', '789']
# ss = " ".join(l)

m = {"john" : "ss"}
m.update({"john" : "ss"})
m.update({"john" : "mm"})
m.update({'run' : 'ss'})
ll = {item[0] : item[1] for item in m.items() if item[0] != 'run'}
print(ll)
# print(ll)
