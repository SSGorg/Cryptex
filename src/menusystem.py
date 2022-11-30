import curses
# Windows: python3 -m pip install windows-curses
# Unix: it's preinstalled

class MenuSystem:
    def __init__(self, cipher_list):
        self.sort_ciphers(cipher_list)
        # Manually initialize curses
        self.curses_init()
        
        # Start menu, and handle exceptions
        try:
            self.last_key = ''
            self.curses_menu()
        except KeyboardInterrupt:
            pass
        
        # Manually deinitialize curses
        self.curses_end()

    def curses_init(self):
        # BEGIN ncurses startup/initialization...
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        curses.curs_set(False)
        if curses.has_colors():
            curses.start_color()
        # stdscr.keypad(True)
        # END ncurses startup/initialization...

    def curses_end(self):
        # BEGIN ncurses shutdown/deinitialization...
        curses.nocbreak()
        curses.echo()
        curses.curs_set(True)
        # stdscr.keypad(False)
        curses.endwin()
        # END ncurses shutdown/deinitialization...

    def input_handler(self):
        self.last_key = chr(self.stdscr.getch())
        return True

    def center(self, width, msg):
        return (width // 2) - (len(msg) // 2)

    def line(self, line, width, char):
        string = width * char
        self.stdscr.addstr(line, self.center(width, string), string)

    def header(self, line, text):
        (height, width) = self.stdscr.getmaxyx()
        
        self.line(line - 1, width, '-')
        
        self.stdscr.addstr(line, self.center(width, text), text)

        self.line(line + 1, width, '-')
        
    def menu_cipher_types(self):
        (height, width) = self.stdscr.getmaxyx()

        self.header(1, 'Cryptex')
        self.header(10, 'Cipher Types')

        offset = 13
        self.selected_type = ''
        
        for i, cipher_type in enumerate(self.types.keys()):
            flag = False
            if i == (self.selection % len(self.types.keys())):
                self.stdscr.attron(curses.color_pair(1))
                self.selected_type = cipher_type
                flag = True
            self.stdscr.addstr(offset + i, self.center(width, cipher_type), cipher_type)
            if flag:
                self.stdscr.attroff(curses.color_pair(1))

        self.line(offset + len(self.types.keys()) + 1, width, '-')

        return 1

    def menu_ciphers(self):
        (height, width) = self.stdscr.getmaxyx()

        self.header(1, 'Cryptex')
        self.header(10, self.selected_type + 's')

        offset = 13

        for i, cipher in enumerate(self.types[self.selected_type]):
            flag = False
            if i == (self.selection % len(self.types[self.selected_type])):
                self.stdscr.attron(curses.color_pair(1))
                flag = True
            self.stdscr.addstr(offset + i, self.center(width, cipher.name), cipher.name)
            if flag:
                self.stdscr.attroff(curses.color_pair(1))

        self.line(offset + len(self.types[self.selected_type]) + 1, width, '-')

        return 0
                
    # start curses menu
    def curses_menu(self):
        self.states = [self.menu_cipher_types, self.menu_ciphers]
        self.state = 0
        self.selection = 0

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        
        self.stdscr.clear()
        self.stdscr.refresh()
        while True:
            (height, width) = self.stdscr.getmaxyx()
            msgs = [
                "Press 'w', or 's' to move the selection up/down.",
                "Press ' ' to select an option",
                "Press 'q' to quit",
                ]
            for i, msg in enumerate(msgs):
                self.stdscr.addstr(3 + i, self.center(width, msg), msg)
            
            next_state = self.states[self.state % len(self.states)]()

            self.input_handler()

            if 'q' == self.last_key:
                break

            elif 'w' == self.last_key:
                self.selection -= 1

            elif 's' == self.last_key:
                self.selection += 1

            elif ' ' == self.last_key:
                self.selection = 0
                self.state = next_state

            self.stdscr.clear()
            self.stdscr.refresh()
        
    # sort the ciphers by type
    def sort_ciphers(self, cipher_list):
        self.types = {}

        for _, cipher in cipher_list.items():
            if not cipher.type in self.types:
                self.types[cipher.type] = []
            self.types[cipher.type].append(cipher)

        
