import os
import requests
from bs4 import BeautifulSoup


# Create a dict of all links to be scraped
# This dict will also be used to create the csv files that will hold pin definitions
links = { 
    "nRF9160" : "https://infocenter.nordicsemi.com/topic/ps_nrf9160/pin.html",
    "nRF7002" : "https://infocenter.nordicsemi.com/topic/ps_nrf7002/chapters/hw_layout/doc/hw_layout.html",
    "nRF5340" : "https://infocenter.nordicsemi.com/topic/ps_nrf5340/chapters/pin.html?cp=4_0_0_8_0",
    "nRF52840" : "https://infocenter.nordicsemi.com/topic/ps_nrf52840/pin.html",
    "nRF52833" : "https://infocenter.nordicsemi.com/topic/ps_nrf52833/pin.html",
    "nRF52832" : "https://infocenter.nordicsemi.com/topic/com.nordic.infocenter.nrf52832.ps.v1.1/pin.html?cp=5_2_0_3#pin_assign",
    "nRF52820" : "https://infocenter.nordicsemi.com/topic/ps_nrf52820/pin.html",
    "nRF52811" : "https://infocenter.nordicsemi.com/topic/ps_nrf52811/pin.html",
    "nRF52810" : "https://infocenter.nordicsemi.com/topic/ps_nrf52810/pin.html",
    "nRF52805" : "https://infocenter.nordicsemi.com/topic/ps_nrf52805/pin.html",
    "nRF21540" : "https://infocenter.nordicsemi.com/topic/ps_nrf21540/chapters/hw_layout/pin/doc/frontpage.html",
    "nPM6001" : "https://infocenter.nordicsemi.com/topic/ps_npm6001/chapters/hw_layout/pin/doc/frontpage.html",
    "nPM1100" : "https://infocenter.nordicsemi.com/topic/ps_npm1100/chapters/pin.html",
}

footprints = {
    "nRF9160" : ["LGA",],
    "nRF7002" : ["QFN48",],
    "nRF5340" : ["aQFN94", "WLCSP",],
    "nRF52840" : ["aQFN73", "QFN48", "WLCSP",],
    "nRF52833" : ["aQFN73", "QFN40", "WLCSP",],
    "nRF52832" : ["QFN48", "WLCSP",],
    "nRF52820" : ["QFN40", "WLCSP",],
    "nRF52811" : ["QFN48", "QFN32", "WLCSP",],
    "nRF52810" : ["QFN48", "QFN32", "WLCSP",],
    "nRF52805" : ["WLCSP",],
    "nRF21540" : ["QFN16"],
    "nPM6001" : ["WLCSP",],
    "nPM1100" : ["WLCSP", "QFN24",],
}

# For each link in the dict, enumerate all of the tables and save them to individual files
# in a new directory. If the directory does not exist yet it will be created. 
# The number of tables to be scraped is dependent on the number of footprints for each chip.
# This is because the first table contains the pin definitions for the first footprint and so on.
for link in links:
    # Create a new directory for each chip
    if not os.path.exists(link):
        os.makedirs(link)
    # Request the link and parse the response
    r = requests.get(links[link])
    soup = BeautifulSoup(r.text, "html.parser")
    # Save this file to the directory for reference
    with open(link + "/" + link + ".html", "w", encoding="utf-8") as f:
        f.write(r.text)
    # Get all tables with a caption that contains the word "assignments"
    tables = []
    tables_temp = soup.find_all("table")
    for table in tables_temp:
        if table.find("caption"):
            if "assignments" in table.find("caption").text.lower():
                tables.append(table)
    # For each table get the table body and save it to a file in the new directory
    for i in range(len(tables)):
        # Get the table body
        table_body = tables[i].find("tbody")
        # Now write each row of the table to a csv file
        try:
            with open(link + "/" + link + "_" + footprints[link][i] + ".csv", "w", encoding="utf-8") as f:
                # Write the header
                f.write("Pin number,Pin name,Pin type,Pin description\n")
                # Write each row
                for row in table_body.find_all("tr"):
                    for cell in row.find_all("td"):
                        # Remove all line breaks and commas
                        cell_text = cell.text.strip().replace("\n", "/").replace(",", "")
                        f.write(cell_text + ",")
                    f.write("\n")
        except IndexError:
            print("No footprint defined for " + link)