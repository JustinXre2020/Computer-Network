import os

userinfo = 'userinfo.txt'
userinfo_path = os.path.join(os.getcwd(), userinfo)         # generate userinfo path
mode = 'r+' if os.path.exists(userinfo_path) else 'w+'      # set mode (append & read or write & read) 
                                                            # based on the existance of userinfo
with open(userinfo_path, mode) as f:
    # Get the data from the file
    # f.write("Justin" + ',')
    # f.write("Xiao" + '\n')
    lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
    nested_list = [line.strip().split(',') for line in lines]
    data_list = [data for list in nested_list for data in list]

    # print(f.readlines())
    print(nested_list)
    print(data_list)