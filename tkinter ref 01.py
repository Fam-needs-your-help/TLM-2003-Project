from tkinter import *
from tkinter.ttk import *

class Gui:

    def __init__(self):
        self.root = Tk()
        # Set up the Combobox
        self.selections = Combobox(self.root)
        self.selections['values'] = ['Apples', 'Oranges', 'Blueberries', 'Bananas', 'Custom']
        self.selections.pack()
        # The Entry to be shown if "Custom" is selected
        self.custom_field = Entry(self.root)
        self.show_custom_field = False
        # Check the selection in 100 ms
        self.root.after(100, self.check_for_selection)


    def check_for_selection(self):
        # Checks if the value of the Combobox equals "Custom"
        # Get the value of the Combobox
        value = self.selections.get()
        # If the value is equal to "Custom" and show_field is set to False
        if value == 'Custom' and not self.show_custom_field:
            # Set show_field to True and pack() the custom entry field
            self.show_custom_field = True
            self.custom_field.pack()


        # If the value DOESNT equal "Custom"
        elif value != 'Custom':
            # Set show_field to False
            self.show_custom_field = False
            # Destroy the custom input
            self.custom_field.destroy()
            # Set up a new Entry object to pack() if we need it later.
            # Without this line, tkinter was raising an error for me.
            # This fixed it, but I don't promise that this is the
            # most efficient method to do this.
            self.custom_field = Entry(self.root)

        # If the value IS "Custom" and we're showing the custom_feild
        elif value == 'Custom' and self.show_custom_field:
            pass
        # Call this method again to keep checking the selection box
        self.root.after(100, self.check_for_selection)


app = Gui()
app.root.mainloop()