from battleships import *

from tkinter import *
from tkinter import ttk
import re

current_fleet = randomly_place_all_ships()  # initialize fleet
shots = 0  # initialize shots or "hits"
already_hit = {}  # initialise tuples that have already been hit
types_sunk = {"battleship": [0, " sunk out of 1"],
                "cruiser": [0, " sunk out of 2"],
                    "destroyer": [0, " sunk out of 3"],
                        "submarine": [0, " sunk out of 4"]}  # counter for ships that have been sunk

root = Tk()  # initialize root window
root.title("Battleships")  # title of window

main_box = ttk.Frame(root, borderwidth=5, width=1150, height=600).grid(column=0, row=0, columnspan=23, rowspan=12)

columns_box = ttk.Frame(main_box)  # box for column labels
columns_box.grid(column=2, row=0, rowspan=1, columnspan=10)
rows_box = ttk.Frame(main_box)  # box for row labels
rows_box.grid(column=0, row=2, rowspan=10)

row_axis1 = ttk.Label(rows_box, text="Row Number", anchor=CENTER)  # title of Y axis
row_axis1.grid(column=0, row=5, rowspan=2)
column_axis1 = ttk.Label(columns_box, text="Column Number", anchor=CENTER)  # title of X axis
column_axis1.grid(column=4, row=0)

for i in range(10):
    ttk.Label(main_box, text=str(i)).grid(column=i + 2, row=1)  # initialize column axis marks
    ttk.Label(main_box, text=str(i)).grid(column=1, row=2 + i)  # initialize row axis marks

ship_grid = Canvas(main_box, width=500, height=500, background='white')  # initialize grid to place ships
ship_grid.grid(column=2, row=2, columnspan=10, rowspan=10)
for i in range(0, 500, 50):
    ship_grid.create_line(0, i, 500, i)  # horizontal gridlines
    ship_grid.create_line(i, 0, i, 500)  # vertical gridlines

# initialize interactive box where player will insert hits, count the current hits, count sunk ships, quit or reset.
coord_entry = ttk.Frame(main_box)
coord_entry.grid(column=13, row=3, columnspan=8, rowspan=8)
coord_entry['width'] = 400
coord_entry['height'] = 200
coord_entry['padding'] = 5
coord_entry['borderwidth'] = 1
coord_entry['relief'] = 'sunken'
coord_entry.rowconfigure(3, weight=1, uniform='row')
coord_entry.rowconfigure(4, weight=1, uniform='row')
coord_entry.rowconfigure(5, weight=2, uniform='row')
coord_entry.rowconfigure(6, weight=1, uniform='row')


# validator to ensure that player can only enter values from 0 - 9
def check_num(newval):
    return re.match('^[0-9]*$', newval) is not None and len(newval) <= 1


check_num_wrapper = (root.register(check_num), '%P')

# create row and column entry boxes and their corresponding labels
row = StringVar()
row_entry = ttk.Entry(coord_entry, textvariable=row, validate='key', validatecommand=check_num_wrapper, width=10)
row_entry.grid(column=13, row=3, columnspan=1)
column = StringVar()
column_entry = ttk.Entry(coord_entry, textvariable=column, validate='key', validatecommand=check_num_wrapper, width=10)
column_entry.grid(column=15, row=3, columnspan=1)
row_entry_label = ttk.Label(coord_entry, text="Row Number", anchor=NW)
row_entry_label.grid(column=13, row=4)
column_entry_label = ttk.Label(coord_entry, text="Column Number", anchor=NW)
column_entry_label.grid(column=15, row=4)

# create counters for hits and ships sunk
hits_counter = ttk.Label(coord_entry, text="0")
hits_counter.grid(column=14, row=3)
hits_counter_label = ttk.Label(coord_entry, text="Hits")
hits_counter_label.grid(column=14, row=4)
ships_type_label = ttk.Label(coord_entry, text="Battleships: " + str(types_sunk["battleship"][0]) +
                                                 str(types_sunk["battleship"][1]) + '\n' +
                                                    "Cruisers: " + str(types_sunk["cruiser"][0]) +
                                                    str(types_sunk["cruiser"][1]) + '\n' +
                                                        "Destroyers: " + str(types_sunk["destroyer"][0]) +
                                                        str(types_sunk["destroyer"][1]) + '\n' +
                                                            "Submarines: " + str(types_sunk["submarine"][0]) +
                                                            str(types_sunk["submarine"][1]), justify="right")
ships_type_label.grid(column=14, row=8, rowspan=4)

# dynamic status label, giving player directions of what to do
status = ttk.Label(coord_entry, text="Select a row and column to hit.", wraplength=200)
status.grid(column=13, row=5, columnspan=4)

# initialize variables for images to represent hits and misses
hit_image = PhotoImage(file="images/hit.png")
missed_image = PhotoImage(file="images/missed.png")


def shoot():
    """Executes the shot of row and column entered by the user, and handles the subsequent events afterwards"""
    global shots  # handle the global shows variable
    global current_fleet  # handle the current fleet
    #  return error if row and/or column not input
    if len(row_entry.get()) == 0 and len(column_entry.get()) == 0:
        status['text'] = "You did not enter a column or row number!"
    elif len(row_entry.get()) == 0:
        status['text'] = "You did not enter a row number!"
    elif len(column_entry.get()) == 0:
        status['text'] = "You did not enter a column number!"

    else:  # if input is valid i.e. both row and column entries have values from 0-9 when shot is made
        shots += 1
        hits_counter.configure(text=str(shots))  # increase number of shots by 1
        row_hit = int(row_entry.get())
        column_hit = int(column_entry.get())
        row_entry.delete(0, 'end')  # reset row entry box
        column_entry.delete(0, 'end')  # reset column entry box
        if check_if_hits(row_hit, column_hit, current_fleet) is True:
            current_fleet = hit(row_hit, column_hit, current_fleet)[0]
            """update grid with bomb on row and column hit"""
            already_hit.update({(row_hit, column_hit): ship_grid.create_image((column_hit * 50) + 1, (row_hit * 50) + 1,
                                                                              anchor=NW, image=hit_image)})
            (current_fleet, ship_hit) = hit(row_hit, column_hit, current_fleet)
            if is_sunk(ship_hit):
                for i, j in ship_hit[4]:
                    """update hit squares with letter representing the first letter of the ship type"""
                    already_hit.update({(i, j): ship_grid.create_text(j * 50 + 1, i * 50 + 1,
                                                                      text=ship_type(ship_hit)[0], anchor="nw",
                                                                      fill='red', font=("Helvetica", "16"))})
                types_sunk[str(ship_type(ship_hit))][0] += 1  # update counter of sunk ships
                """update label counting sunk ships"""
                ships_type_label['text'] = ("Battleships: " + str(types_sunk["battleship"][0]) +
                                            str(types_sunk["battleship"][1]) + '\n' +
                                                "Cruisers: " + str(types_sunk["cruiser"][0]) +
                                                str(types_sunk["cruiser"][1]) + '\n' +
                                                    "Destroyers: " + str(types_sunk["destroyer"][0]) +
                                                    str(types_sunk["destroyer"][1]) + '\n' +
                                                        "Submarines: " + str(types_sunk["submarine"][0]) +
                                                        str(types_sunk["submarine"][1]))
                if not are_unsunk_ships_left(current_fleet):
                    """game is complete, disable entry boxes and shots box. Prompt user to reset to play again."""
                    status['text'] = "You sunk all the ships! Press reset to play again."
                    shoot_action['state'] = 'disabled'
                    column_entry.config(state='disabled')
                    row_entry.config(state='disabled')
                else:
                    """ if game is not complete, alert user the type of ship sunk and prompt to make next move """
                    status['text'] = "You sunk a " + ship_type(ship_hit) + "! make your next hit."
            else:
                """ if shit is hit but not sunk, don't reveal the ship type and prompt user to make next hit"""
                status['text'] = "You hit a ship! Make your next hit."
        elif (row_hit, column_hit) in already_hit.keys():
            """if square has already been already hit, alert the user"""
            status['text'] = "You have already hit this square! Make your next hit."
        else:
            """if unrevealed square is hit and it is a miss, alert user that they have missed"""
            status['text'] = "You missed! Make your next hit"
            already_hit.update({(row_hit, column_hit): ship_grid.create_image((column_hit * 50) + 1, (row_hit * 50) + 1,
                                                                              anchor=NW, image=missed_image)})


shoot_action = ttk.Button(coord_entry, text="Shoot!", default="active", command=shoot)
shoot_action.grid(column=14, row=6)
root.bind('<Return>', lambda e: shoot_action.invoke())


def reset():
    """Resets the visualisation and all game-dependent variables, allowing the game to be started again."""
    ship_grid.delete("all")  # deletes everything on the grid canvas
    ship_grid.grid(column=2, row=2, columnspan=10, rowspan=10)
    for i in range(0, 500, 50):
        ship_grid.create_line(0, i, 500, i)  # horizontal gridlines
        ship_grid.create_line(i, 0, i, 500)  # vertical gridlines

    # initialize global variables
    global shots
    global current_fleet
    global already_hit
    global ships_type_label
    global types_sunk
    shots = 0
    hits_counter.configure(text=str(shots))
    current_fleet = randomly_place_all_ships()
    already_hit = {}
    for key, val in types_sunk.items():
        val[0] = 0
    ships_type_label['text'] = ("Battleships: " + str(types_sunk["battleship"][0]) +
                                str(types_sunk["battleship"][1]) + '\n' +
                                    "Cruisers: " + str(types_sunk["cruiser"][0]) +
                                    str(types_sunk["cruiser"][1]) + '\n' +
                                        "Destroyers: " + str(types_sunk["destroyer"][0]) +
                                        str(types_sunk["destroyer"][1]) + '\n' +
                                            "Submarines: " + str(types_sunk["submarine"][0]) +
                                            str(types_sunk["submarine"][1]))
    status['text'] = "Select a row and column to hit."

    # re-enable action buttons and row/column entry
    shoot_action['state'] = 'enabled'
    column_entry.config(state='enabled')
    row_entry.config(state='enabled')


# create reset and quit buttons
reset_button = ttk.Button(coord_entry, text="Reset", default="active", command=reset)
reset_button.grid(column=14, row=12)
quit_button = ttk.Button(coord_entry, text="Quit", default="active", command=root.destroy)
quit_button.grid(column=14, row=13)

root.mainloop()
