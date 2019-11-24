from bysykkel_status_requests import get_table
from tkinter import Tk, Label, Button, ttk, Text


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
