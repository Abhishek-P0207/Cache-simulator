import customtkinter as ctk
from tksheet import Sheet
import Cache_Sim as cs

root = ctk.CTk()
root.geometry("1050x750")
root.resizable(False,False)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue") 

# Some constants for theme 
FONT = ("Roboto",20)
HOVER_COLOUR = "#77C3F5" #Some blue colour
FG_COLOUR = "#CED2DD" #grey colour nearly same as the background colour
BORDER_WIDTH = 3

def page():
#   """This is the function which will be executed when the user press the 'submit' button in home page"""
    global choice_home_page,choice_memory
    choice_home_page = memory_var.get()
    choice_memory = optionmenu_var.get()
    address = address_var.get()
    address = address.zfill(16)
    if choice_home_page == "L1 CACHE":
            Home_page.destroy()
            l1_interface(address)
    if choice_home_page == "L2 CACHE":
        Home_page.destroy()
        l2_interface(address)
    if choice_home_page == "VICTIM CACHE":
        Home_page.destroy()
        vic_interface(address)
    if choice_home_page=="HOME" and choice_memory=="LOAD":
        cs.l1_read(address)

#Home page
def home():
    global Home_page,address_var,memory_var,optionmenu_var
    Home_page = ctk.CTkFrame(root,height=750,width=1050)
    root.title("Cache Simulator")
    optionmenu_var = ctk.StringVar()
    optionmenu_var.set("STORE")
    memory_var = ctk.StringVar()
    memory_var.set("HOME")
    address_var = ctk.StringVar()

    ctk.CTkLabel(Home_page,
                text="Choose :",
                justify=ctk.CENTER,
                font=FONT).place(x=20,y=20)   
    ctk.CTkOptionMenu(Home_page,
                        values=["STORE","LOAD"],
                        variable=optionmenu_var,
                        width=175,
                        height=40,
                        dropdown_hover_color= HOVER_COLOUR,
                        font= FONT,  
                        ).place(x=430,y=20)
    ctk.CTkLabel(Home_page, text="Enter the memory address(binary):",
                font=FONT   
                ).place(x=20,y=165)
    ctk.CTkEntry(Home_page,
                textvariable=address_var,
                font=FONT,  
                width=200).place(x=430,y=165)
    button = ctk.CTkButton(Home_page,
                        text="Submit",
                        corner_radius=15,
                        command=page,
                        border_width = BORDER_WIDTH,
                        font=FONT,
                        border_color= HOVER_COLOUR,
                        hover_color= HOVER_COLOUR,
                        fg_color=FG_COLOUR)
    button.place(x=430,y=500)
    ctk.CTkLabel(Home_page,
                text="SHOW :",
                font = FONT
                ).place(x=20,y=300)
    ctk.CTkOptionMenu(Home_page,
                        values=["L1 CACHE","VICTIM CACHE","L2 CACHE"],
                        variable=memory_var,
                        width=175,
                        height=40,
                        dropdown_hover_color= HOVER_COLOUR,
                        font= FONT,  
                        ).place(x=430,y=300)
    Home_page.pack(fill="both",padx=30,pady=30)
home()

def go_home_1():
    l1_interface_frame.destroy()
    home()
def go_home_2():
    l2_interface_frame.destroy()
    home()
def go_home_3():
    vic_interface_frame.destroy()
    home()

def l1_interface(address):
    global l1_interface_frame,data_c
    if(choice_memory=="STORE"):
        cs.l1_write(address)
    else:
        data_c = cs.l1_read(address)
    root.title("L1 CACHE")
    root.geometry("1050x750")
    l1_interface_frame = ctk.CTkFrame(root)
    sheet = Sheet(l1_interface_frame, data=[[f"{cs.l1[r][-1]}" for c in range(64)] for r in range(128)])
    sheet.pack(fill="both", expand=True,padx=30,pady=50)
    ctk.CTkButton(l1_interface_frame,
                    text='HOME',
                    command=go_home_1,
                    border_width = BORDER_WIDTH,
                    font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=450,y=0)
    l1_interface_frame.pack(fill="both",padx=30,pady=30,expand = True)

def l2_interface(address):
    global l2_interface_frame,data_c
    if(choice_memory=="STORE"):
        cs.l2_write(address)
    else:
        data_c = cs.l2_read(address)
    # Home_page.destroy()
    root.title("L2 CACHE")
    root.geometry("1050x750")
    l2_interface_frame = ctk.CTkFrame(root,height=750,width=750)
    sheet = Sheet(l2_interface_frame, data=[[f"{cs.l2[r][-1]}" for c in range(64)] for r in range(256)])
    sheet.pack(fill="both", expand=True,padx=30,pady=50)
    ctk.CTkButton(l2_interface_frame,
                    text='HOME',
                    command=go_home_2,
                    border_width = BORDER_WIDTH,
                    font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=450,y=0)
    l2_interface_frame.pack(fill="both",padx=30,pady=30,expand = True)

def vic_interface(address):
    global vic_interface_frame,data_c
    if(choice_memory=="STORE"):
        cs.write_victim(address)
    else:
        data_c = cs.read_victim(address)
    root.title("VICTIM CACHE")
    root.geometry("1050x750")
    vic_interface_frame = ctk.CTkFrame(root,height=750,width=750)
    sheet = Sheet(vic_interface_frame, data=[[f"{cs.vic[r][-1]}" for c in range(64)] for r in range(4)])
    sheet.pack(fill="both", expand=True,padx=30,pady=50)
    ctk.CTkButton(vic_interface_frame,
                    text='HOME',
                    command=go_home_3,
                    border_width = BORDER_WIDTH,
                    font=FONT,
                    border_color= HOVER_COLOUR,
                    hover_color= HOVER_COLOUR,
                    fg_color=FG_COLOUR).place(x=450,y=0)
    vic_interface_frame.pack(fill="both",padx=30,pady=30,expand = True)

root.mainloop()