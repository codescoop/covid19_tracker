import requests
from bs4 import BeautifulSoup


def get_html_data(url):
    page_html = requests.get(url)
    soup = BeautifulSoup(markup=page_html.text, features="html.parser")
    # print(soup.prettify())
    return soup


## Function to web scrap covid details.
def fetch_covid19_detail(soup):
    # page_html = requests.get(url)
    # soup = BeautifulSoup(markup=page_html.text, features="html.parser")
    # print(soup.find("div", class_="site-stats-count").prettify())

    duration = soup.find("div","status-update").span.text
    # print("Database Last Updated",duration[3:])

    info_block = soup.find("div", "site-stats-count").find_all("li")
    # print(len(info_block))
    for index in range(len(info_block)-1):
        stat=info_block[index].find("strong").text
        header=info_block[index].find("span").get_text()
        # print(header,":",stat)


## Function to get Statewise statistics
def fetch_statewise_detail(soup):

    # print(soup.find("table", class_="table table-striped").thead.prettify())
    # print(soup.find("table", class_="table table-striped").tbody.prettify())
    # state_info_table = soup.find("table", class_="table table-striped").tbody.find_all("td")

    state_stat = []

    state_info_table = soup.select("table.table.table-striped>tbody>tr>td")
    # print(state_info_table)
    # print(len(state_info_table))
    for index in range(len(state_info_table)-16):
        # print(state_info_table[index].text)
        state_stat.append(state_info_table[index].text)
    print(state_stat)

    ## Searching State ----------------------------------
    state="Andaman and Nicobar Islands"
    for i in range(len(state_stat)):
        if(state_stat[i]==state):
            print(state_stat[i])
            print(state_stat[i+1])
            print(state_stat[i + 2])
            print(state_stat[i + 3])
            print(state_stat[i + 4])
            break


## Main Function
def main():
    url="https://www.mohfw.gov.in/"
    html_soup = get_html_data(url)
    fetch_covid19_detail(html_soup)
    fetch_statewise_detail(html_soup)


if __name__== "__main__":
    main()
