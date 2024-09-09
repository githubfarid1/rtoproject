from os import system, name
from pathlib import Path
import sys
from prettytable import PrettyTable
from subprocess import Popen, check_call, PIPE, STDOUT
from sys import platform
xproxies = {
  "http": "http://scrapeops.country=us:c58f3885-5149-4c03-8a3a-1b2d3ffba3c6@residential-proxy.scrapeops.io:8181",
  "https": "http://scrapeops.country=us:c58f3885-5149-4c03-8a3a-1b2d3ffba3c6@residential-proxy.scrapeops.io:8181"
}

if platform == "win32":
	from subprocess import CREATE_NEW_CONSOLE

def run_module(comlist):
	if platform == "linux" or platform == "linux2":
		comlist[:0] = ["--"]
		comlist[:0] = ["gnome-terminal"]
		# print(comlist)
		proc = Popen(comlist)
	elif platform == "win32":
		proc = Popen(comlist, creationflags=CREATE_NEW_CONSOLE)
		print(proc.pid)

	comall = ''
	for com in comlist:
		comall += com + " "
	print(comall)

def clear_screen():
    if name == 'nt':
        clear = lambda: system('cls')
    else:
        clear = lambda: system('clear')
    clear()

def main():
    while True:
        clear_screen()
        myTable = PrettyTable(["NO","MENU"])
        myTable.align ="l"
        myTable.add_row(["1", "Scrape RTO List"])
        myTable.add_row(["2", "Scrape Seek.com"])
        myTable.add_row(["X", "Exit"])

        print(myTable)
        choice = input("Input Your Choice: ")
        if choice == "1":
            rtolist()
        elif choice in ('x', 'X'):
            sys.exit()

def rtolist():
    while True:
        clear_screen()
        myTable = PrettyTable()
        myTable.align ="c"
        myTable.add_column("Module",["Scrape RTO List"])
        # myTable.add_row(["Scrape RTO List"])
        print(myTable)
        filename = input("Input Filename: ")
        filename = f"fileresult/{filename}"
        if filename[-4:] not in ('xlsx','XLSX'):
            print("Please input xlsx file")
            continue
        if Path(filename).exists():
            yesno = input(f"File {filename} is exists. do you want to replace it [Y/N]? ")
            if yesno in ('y', 'Y'):
                break         
            else:
                sys.exit()
        break
    
    proxy = input("Input Proxy (Optional): ")


if __name__ == '__main__':
    main()
