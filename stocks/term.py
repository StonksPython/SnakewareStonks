import sys
import traceback

from io import StringIO

import pygame
import pygame_gui
import pandas as pd

from pygame_gui.elements import UITextBox


class stocks(pygame_gui.elements.UIWindow):
    def __init__(self, pos, manager):
        super().__init__(
            pygame.Rect(pos, (400, 300)),
            manager,
            window_display_title="Stock Prices",
            object_id="#stocks",
            resizable=True,
        )
        bob = "AAPL"
        string = (
            'df = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="'
            + bob
            + '"&apikey=WCXVE7BAD668SJHL&datatype=csv")\nprint("Open: ", end=" ")\nprint(df["Open"][0])\nprint("Close: ", end=" ")\nprint(df["Close"][0])'
        )
        print(string)
        self.instructions = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect(0, 0, 368, 50),
            text="Type in a NYSE Stock Symbol to get Started!",
            manager=manager,
            container=self,
            object_id="#intructions",
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        self.textbox = pygame_gui.elements.UITextBox(
            "",
            relative_rect=pygame.Rect(0, 50, 368, 150),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "top",
                "bottom": "bottom",
            },
        )
        self.input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect(0, -35, 368, 30),
            manager=manager,
            container=self,
            anchors={
                "left": "left",
                "right": "right",
                "top": "bottom",
                "bottom": "bottom",
            },
        )

    def set_text(self, text):
        self.textbox.html_text = text.replace("\n", "<br>")
        self.textbox.rebuild()

    def append_text(self, text):
        self.textbox.html_text = self.textbox.html_text + text.replace("\n", "<br>")
        self.textbox.rebuild()

    def process_event(self, event):
        super().process_event(event)

        def stringInText(name):
            str = 'import pandas as pd\ndf = pd.read_csv("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='
            str += name
            str += '&apikey=WCXVE7BAD668SJHL&datatype=csv")\nprint("Open: ", end=" ")\nprint(df["Open"][0])\nprint("Close: ", end=" ")\nprint(df["Close"][0])'
            return str

        if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
            _stdout = sys.stdout
            sys.stdout = tout = StringIO()

            try:
                name = self.input.get_text()
                print(name)

                temp = stringInText(name)
                print(temp)
                code = compile(temp, "stocks_code", "exec")
                exec(code, globals())
            except Exception:
                e_type, e_val, e_traceback = sys.exc_info()
                print("Traceback (most recent call last):")
                traceback.print_tb(e_traceback, None, tout)
                print(e_type, e_val)

            sys.stdout = _stdout
            result = tout.getvalue()
            self.append_text(result)
            self.input.set_text("")
