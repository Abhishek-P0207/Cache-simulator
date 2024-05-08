# L1 cache
l1_lines = 128
valid_bit = 0
block_size = 64
l1_count = 0
data = None 
# valid bit , dirty bit , byte_off, data
l1 = []
for i in range(128):
    l1.append([-1,0,-1,None])

# victim cache 
vic_lines = 4
vic_tag = 0
vic_count = 0
vic_data = None
# valid , tag , count , data
vic = []
for i in range(4):
    vic.append([0,-1,-1,None])

# L2 cache
l2_lines_no = 256
l2_set_off = 0
l2_count = 0
data = None 
# valid , byte_off , data
l2 = []
for i in range(l2_lines_no):
    l2.append([-1,-1,None])


def byte_offset(address):
    byte_off = int(address[10:],2)
    return byte_off

def l1_line_off(address):
        block_offset = int(address[:10],2)
        return block_offset

def l2_set_off(address):
    set_off = int(address[4:10],2)
    return set_off

def vic_tag(address):
    tag = int(address[:10],2)
    return tag


def lru(arr):
    min = 20  
    index = -1
    for i in range(len(arr)):
        if(arr[2]<min):
            min = arr[2]
            index = i
    return index

# victim : valid ,tag,count,data
def write_victim(address):
    flag = 0
    for i in range(4):
        if(vic[i][0]==0):
            vic[i]= [1,vic_tag(address),1,l1_line_off(address)]
            flag = 1
            break
    if(flag==0):
        to_be_removed_i = lru(vic)
        vic[to_be_removed_i] = [0,-1,-1,None]
        write_victim(address)

def read_victim(address):

    for i in range(4):
        if(vic[i][0]==1 and vic[i][1]==vic_tag(address)):
            vic[i][2] = vic[i][2] + 1
            l1_write[address]
            print("Available in victim")
    else:
        print("Not available in victim.. Checking in L2\n")
        l2_read(address)

# valid bit , dirty bit , byte_off ,, data
def l1_write(address):
    prev_address = -1
    if(prev_address != address):
        data = l1_line_off(address)
        l1[l1_line_off(address)%128] = [1 , 0 , byte_offset(address), data]
        prev_address = address
        
    elif(l1_line_off(prev_address)%128 == l1_line_off(address)%128):
        write_victim(prev_address)

def l1_read(address):
    print("L1 read\n")
    line_offset = l1_line_off(address)%128
    if(l1[line_offset][0]==1 and l1[line_offset][-2]==byte_offset(address)):
        l_data = l1[line_offset]
        l1[line_offset][1]=1   #setting dirty bit
        print(f"The data is available in L1 and data is {l1[line_offset][3]}")
    else:
        print("Not available in L1.. Searching in Victim cache \n")
        read_victim(address)

def l2_write(address):
    flag = 0
    data = l1_line_off(address)
    l2_set_no = l2_set_off(address)
    # print(l2_set_no)
    for i in range(4):
        if(l2[l2_set_no*4 + i][0] == -1):
            l2[l2_set_no*4+i] = [1 ,byte_offset(address),data]
            break

def l2_read(address):
    flag = 1
    print("L2 read\n")
    for i in range(4):
        if(l2[l2_set_off(address)][0]==1 and l2[l2_set_off(address)][1] == byte_offset(address) and l2[l2_set_off(address)][2] == l1_line_off(address)):
            flag = 0
            print(f"Data Available in L2 and data - {l2[l2_set_off(address)][2]}")
    # l1_write(address)
    if(flag==1):
        print("Data not available in L2.. Searching in Main Memory\n")
        mm_read(address)

def mm_read(address):
    l2_write(address)
    l1_write(address)
    print("Data available in Main Memory,Data written into other cache.\n\n")

