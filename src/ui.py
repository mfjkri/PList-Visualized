import os
from tkinter import (W, X, Y, Tk, Label, Frame, LabelFrame, Radiobutton, Button, PhotoImage,
                     IntVar, BOTH, BOTTOM, NORMAL, DISABLED)

LARGE_LARGE_FONT = ("Segoe UI", 30, "bold")
LARGE_FONT = ("Segoe UI", 16, "bold")
NORM_FONT = ("Segoe UI", 26, "bold")
SMALL_FONT = ("Segoe UI", 8)

WHITE, GREY, DARK_GREY, BLACK, RED, BLUE, GREEN, PURPLE = ("#ffffff",  # WHITE
                                                           "#bcbcbc",  # GREY
                                                           "#222222",  # DARK_GREY
                                                           "#000000",  # BLACK
                                                           "#660000",  # RED
                                                           "#2986cc",  # BLUE
                                                           "#007F66",  # GREEN
                                                           "#6a329f")  # PURPLE

BUTTON_WIDTH, BUTTON_HEIGHT = 10, 1


class UI:
    def __init__(self, width: int, height: int) -> None:
        self.root = Tk()
        self.root.title("PLIST Visualizer")
        self.root.geometry(f"{width}x{height}")
        self.root.configure(bg=DARK_GREY)

        self.radio_buttons = []
        self.cached_radio_options = {}
        self.current_page = 0
        self.current_name = ""

        self.present_participants_dict: dict = None
        self.setup()

    def setup(self) -> None:

        self.frame1 = Label(self.root, bg='#B71C1C', borderwidth=0)
        self.frame1.pack()

        self.choices_frame = LabelFrame(
            self.frame1, text='-', font=LARGE_LARGE_FONT, bg=DARK_GREY, fg=WHITE, padx=30, pady=20, borderwidth=0)
        self.choices_frame.pack(fill=BOTH)

        self.buttons_frame = Frame(self.root, bg=DARK_GREY)
        self.buttons_frame.pack(side=BOTTOM)

        self.buttons_grid = Frame(self.buttons_frame, bg=DARK_GREY)
        self.buttons_grid.pack(fill=X)

        self.delete_btn = Button(
            self.choices_frame, text="DELETE", command=self.delete_participant, font=NORM_FONT,
            bg=RED,)
        self.delete_btn.pack()

        self.prev_btn = Button(
            self.buttons_grid, text="Prev", command=self.prev_page, font=NORM_FONT,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT, borderwidth=0)
        self.prev_btn.grid(row=0, column=0, padx=15)

        self.next_btn = Button(
            self.buttons_grid, text="Next", command=self.next_page, font=NORM_FONT,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT, borderwidth=0)
        self.next_btn.grid(row=0, column=1, padx=15)

        self.submit_btn = Button(
            self.buttons_grid, text="Submit", command=self.next_page, font=NORM_FONT,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg=GREEN, borderwidth=0)
        self.submit_btn.grid(row=0, column=2, padx=15)

    def add_radio_button(self, text: str, var: IntVar, value: int, color: int = GREY) -> None:
        radio_button = Radiobutton(
            self.choices_frame, text=text, font=LARGE_FONT,
            variable=var, value=value,
            bg=color, activebackground=PURPLE, activeforeground=WHITE,
            borderwidth=0, pady=10)
        radio_button.pack(pady=5, anchor=W)
        radio_button.bind("<Button-3>", lambda e,
                          w=radio_button: self.delete_radio_button(w))
        self.radio_buttons.append(radio_button)

    def delete_radio_button(self, w: Radiobutton) -> None:
        self.present_participants_dict[self.current_name].remove(
            w["text"][:-3])
        self.radio_buttons.remove(w)
        w.pack_forget()

    def clear_radio_buttons(self) -> None:
        for radio_button in self.radio_buttons:
            radio_button.pack_forget()

    def next_page(self) -> None:
        self.current_page += 1
        self.display()

    def prev_page(self) -> None:
        self.current_page -= 1
        self.display()

    def display(self) -> None:
        self.clear_radio_buttons()

        self.current_name = self.matched_participants[self.current_page]

        var = IntVar(
        ) if not self.current_name in self.cached_radio_options else self.cached_radio_options[self.current_name]
        self.cached_radio_options.update({self.current_name: var})

        for idx, matched_names in enumerate(self.present_participants_dict[self.current_name]):
            self.add_radio_button(matched_names + "   ", var, idx, GREEN)

        self.prev_btn['state'] = DISABLED if self.current_page == 0 else NORMAL
        self.next_btn['state'] = DISABLED if self.current_page == len(
            self.matched_participants) - 1 else NORMAL

        if True:
            self.submit_btn['state'] = DISABLED

        self.choices_frame.config(text=self.current_name)

    def delete_participant(self) -> None:
        self.present_participants_dict.pop(self.current_name)

        self.update_matched_participants()

        self.cached_radio_options.pop(self.current_name)

        if self.current_page + 1 >= len(self.matched_participants) - 1:
            self.prev_page()
        else:
            self.display()

    def start(self, present_participants_dict: dict) -> None:
        self.present_participants_dict = present_participants_dict
        self.matched_participants = self.update_matched_participants()
        self.display()
        self.root.mainloop()

    def update_matched_participants(self) -> None:
        self.matched_participants = list(self.present_participants_dict.keys())
        self.matched_participants.sort()
        return self.matched_participants
