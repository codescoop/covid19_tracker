import requests
from bs4 import BeautifulSoup
import tkinter as tk
import plyer
import threading
import datetime
import time


def get_html_data(url):
    page_html = requests.get(url)
    soup = BeautifulSoup(markup=page_html.text, features="html.parser")
    # print(soup.prettify())
    return soup


## Function to web scrap covid details-------------------------------
def fetch_covid19_detail(soup):
    # print(soup.find("div", class_="site-stats-count").prettify())
    # duration = soup.find("div", "status-update").span.text
    info_block = soup.find("div", "site-stats-count").find_all("li")
    # print(len(info_block))
    stat_list=[]
    for index in range(len(info_block) - 1):
        stat = info_block[index].find("strong").text
        header = info_block[index].find("span").get_text()
        # print(header, ":", stat)
        stat_list.append(stat)
    # print(stat_list)
    caseslabel2["text"] = stat_list[0]  ## Active Cases
    curedlabel2["text"] = stat_list[1]  ## Cured/Discharged/Migrated
    deathlabel2["text"] = stat_list[2]  ## Deaths
    confirmedlabel2["text"] = stat_list[3]  ## Total Confirmed cases

## Function to get Statewise statistics---------------------------
def fetch_statewise_detail(soup,state_name):
    # print(soup.find("table", class_="table table-striped").thead.prettify())
    # print(soup.find("table", class_="table table-striped").tbody.prettify())
    # state_info_table = soup.find("table", class_="table table-striped").tbody.find_all("td")
    state_stat = []
    state_info_table = soup.select("table.table.table-striped>tbody>tr>td")
    # print(state_info_table)
    # print(len(state_info_table))
    for index in range(len(state_info_table) - 16):
        # print(state_info_table[index].text)
        state_stat.append(state_info_table[index].text)
    # print(state_stat)

    ## Searching State ----------------------------------
    # state = "Andaman and Nicobar Islands"
    notify_list = []
    state = state_name
    for i in range(len(state_stat)):
        if (state_stat[i] == state):
            # regionlabel2["text"] = state_stat[i]       ## Name of State / UT
            caseslabel2["text"] = state_stat[i + 1]     ## Active Cases
            curedlabel2["text"] = state_stat[i + 2]     ## Cured/Discharged/Migrated
            deathlabel2["text"] = state_stat[i + 3]       ## Deaths
            confirmedlabel2["text"] = state_stat[i + 4]    ## Total Confirmed cases
            for x in range(0,5):
                notify_list.append(state_stat[i+x])
            return notify_list
            # break

## Function to get state from dropdown
def getstate(state_name):
    global current_region
    current_region=state_name
    fetch_statewise_detail(html_soup, current_region)

def set_notification():
    # Creating a new thread --------------
    th1=threading.Thread(target=get_notification())
    th1.setDaemon(True)
    th1.start

def refresh():
    print("refreashing")
    html_soup = get_html_data(url)
    fetch_statewise_detail(html_soup, current_region)

def get_notification():
    reminder_duration = int(notify_inp.get())
    if current_region == "INDIA":
        plyer.notification.notify(
            title="COVID19 Detail of INDIA",
            message="Please select STATE to view Statistics.",
            timeout=3,
            app_icon="img/notify.ico"
        )

    else:
        data = fetch_statewise_detail(html_soup, current_region)
        plyer.notification.notify(
                            title="COVID19 Detail of "+data[0],
                            message = "Active Cases : "+data[1]+"\nCured Cases : "+data[2]+"\nDeath Cases : "+data[3]+"\nConfirmed Cases : "+data[4],
                            timeout=10,
                            app_icon="img/notify.ico"
                          )
        time.sleep(reminder_duration)
	#refresh()

if __name__ == "__main__":
    ## Creating GUI ---------------------
    root = tk.Tk()
    root.geometry("745x350")
    root.title("LIVE:Covod19 Tracker INDIA - [YYSCOOP.com]")
    root.iconbitmap("img/favicon.ico")
    root.resizable(0, 0)
    root.config(bg="black")

    ## Style Setting ----------------
    bgcolor = "black"
    fgcolor = "white"
    keylabel_width = 25
    valuelabel_width = 30
    Hfont = ("poppins", 10, "bold")
    Lfont = ("poppins", 10, "bold")

    ## Image --------------------
    img = tk.PhotoImage(file=r"img\covid19.png")
    imgLabel = tk.Label(root, image=img, width="280", height="330", bg="black", fg="white")
    imgLabel.grid(row=0, rowspan=7, column=0, sticky=tk.W, padx=0, pady=5)

    ## Region Label --------------------
    regionlabel1 = tk.Label(root, text="COUNTRY / STATE / UT :", font=Lfont, bg=bgcolor, fg=fgcolor, width=keylabel_width)
    regionlabel1.grid(row=0, column=1, sticky=tk.W, padx=0, pady=5)

    region = ["Andhra Pradesh","Arunachal Pradesh ","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu","Lakshadweep","National Capital Territory of Delhi","Puducherry"]
    current_region = "INDIA"
    variable = tk.StringVar(root)
    variable.set("INDIA")  # default value
    regionlabel2 = tk.OptionMenu(root, variable,*region,command=getstate)
    regionlabel2.config(width= valuelabel_width,bg=bgcolor, fg=fgcolor)
    regionlabel2.grid(row=0, column=2, columnspan=3, sticky=tk.W, padx=0, pady=5)

    ## Cases Label --------------------
    caseslabel1 = tk.Label(root, text="ACTIVE CASES :", font=Lfont, bg=bgcolor, fg=fgcolor, width=keylabel_width)
    caseslabel1.grid(row=1, column=1, sticky=tk.W, padx=0, pady=5)

    caseslabel2 = tk.Label(root, text="xxxxxxx", font=Lfont, bg=bgcolor, fg=fgcolor, width=valuelabel_width)
    caseslabel2.grid(row=1, column=2, columnspan=3, sticky=tk.W, padx=0, pady=5)

    ## Cured Label --------------------
    curedlabel1 = tk.Label(root, text="CURED CASES :", font=Lfont, bg=bgcolor, fg=fgcolor, width=keylabel_width)
    curedlabel1.grid(row=2, column=1, sticky=tk.W, padx=0, pady=5)

    curedlabel2 = tk.Label(root, text="xxxxxxx", font=Lfont, bg=bgcolor, fg=fgcolor, width=valuelabel_width)
    curedlabel2.grid(row=2, column=2, columnspan=3, sticky=tk.W, padx=0, pady=5)

    ## Death Label --------------------
    deathlabel1 = tk.Label(root, text="DEATHS CASES:", font=Lfont, bg=bgcolor, fg=fgcolor, width=keylabel_width)
    deathlabel1.grid(row=3, column=1, sticky=tk.W, padx=0, pady=5)

    deathlabel2 = tk.Label(root, text="xxxxxxx", font=Lfont, bg=bgcolor, fg=fgcolor, width=valuelabel_width)
    deathlabel2.grid(row=3, column=2, columnspan=3, sticky=tk.W, padx=0, pady=5)

    ## Confirmed Label --------------------
    confirmedlabel1 = tk.Label(root, text="CONFIRMED CASES :", font=Lfont, bg=bgcolor, fg=fgcolor, width=keylabel_width)
    confirmedlabel1.grid(row=4, column=1, sticky=tk.W, padx=0, pady=5)

    confirmedlabel2 = tk.Label(root, text="xxxxxxx", font=Lfont, bg=bgcolor, fg=fgcolor, width=valuelabel_width)
    confirmedlabel2.grid(row=4, column=2, columnspan=3, sticky=tk.W, padx=0, pady=5)

    ## Notification Label --------------------
    notifylabel1 = tk.Label(root, text=" DESKTOP NOTIFICATION :", font=Lfont, bg="grey", fg=fgcolor, width=keylabel_width)
    notifylabel1.grid(row=5, column=1, sticky=tk.W, padx=0, pady=5)
    notify_inp = tk.Entry(root, font=Lfont, bg=bgcolor, fg=fgcolor, justify='center',bd=1, width=7)  # Textbox - Input
    notify_inp.insert(tk.END, '120')
    notify_inp.grid(row=5, column=2, padx=0, pady=5)
    minlabel = tk.Label(root, text="minutes", font=Lfont, bg=bgcolor, fg=fgcolor, width=5)
    minlabel.grid(row=5, column=3, padx=0, pady=2, sticky=tk.W)
    notifyBtn = tk.Button(root, text="START", font=Lfont, bg="#006699", fg=fgcolor, width=10,command=set_notification)
    notifyBtn.grid(row=5, column=4, padx=0, pady=2)

    ## URL & Date Label --------------------
    datelabel1 = tk.Label(root, text="SOURCE : https://www.mohfw.gov.in/   |    " + str(datetime.datetime.now()),font=Hfont, bg=bgcolor, fg="red")
    datelabel1.grid(row=6, column=1, columnspan=4, sticky=tk.W, padx=0, pady=5)

    ## Function Calls --------------------
    url = "https://www.mohfw.gov.in/"
    html_soup = get_html_data(url)
    fetch_covid19_detail(html_soup)

    root.mainloop()


