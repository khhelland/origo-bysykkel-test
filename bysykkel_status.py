import requests
import json
from tkinter import Tk, Label, Button, ttk, Text

def get_table():

    table = []
    data_received = False

    try:
        response_status = requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"
                                       , headers={"client-name": "personlig-bysykkel_status"})
        response_info = requests.get("https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
                                     , headers={"client-name": "personlig-bysykkel_status"})
    except requests.exceptions.ConnectionError:
        print("Could not connect to bysykkel-API")
        return table, data_received

    if response_status.status_code==200 and response_info.status_code==200:
        try:
            for station_info in response_info.json()['data']['stations']:
                for station_status in response_status.json()['data']['stations']:
                    if station_info['station_id'] == station_status['station_id']:
                        table.append((station_info['name'],
                                      station_status['num_bikes_available'],
                                      station_status['num_docks_available']
                        ))
                        break
            table.sort(key=lambda x: x[0])
            data_received = True
        except (KeyError, IndexError, TypeError):
            print("Received data not in expected form")
    else:
        print("Unexpected status codes:")
        print("Expected 200 for station status request, received " +str(response_status.status_code))
        print("Expected 200 for station information request, received " + str(response_info.status_code))

    return table, data_received


class BysykkelGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bysykkel status")

        self.table = ttk.Treeview(master,
                                  columns = ("Stasjon", "Ledige sykler", "Ledige låser"),
                                  show='headings')
        self.table.heading("Stasjon", text="Stasjon")
        self.table.heading("Ledige sykler", text="Ledige sykler")
        self.table.heading("Ledige låser", text="Ledige låser")
        self.table.grid(row=1, columnspan=3, sticky="nsew")

        self.message_box = Text(master, height=1)
        self.message_box.grid(row=2, column=1)

        self.update_button = Button(master, text="Oppdater data", command=self.update)
        self.update_button.grid(row=2, column=0)

        self.master.rowconfigure(1, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.update()

    def update_message(self, message):
        self.message_box.delete("1.0", "end")
        self.message_box.insert("end", message)

    def update(self):
        self.update_message("Oppdaterer data")
        new_data, success  = get_table()
        if(success):
            self.table.delete(*self.table.get_children())
            for row in new_data:
                self.table.insert("", "end", values=row)
            self.update_message("Data oppdatert ")
        else:
            self.update_message("Kunne ikke oppdatere data")


if __name__=="__main__":
    root = Tk()
    bysykkelgui = BysykkelGUI(root)
    root.mainloop()
