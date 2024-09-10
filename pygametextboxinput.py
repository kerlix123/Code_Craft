import pygame
import pyperclip

class Textbox:
    def __init__(self, x, y, width, height, font_path):
        pygame.init()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.window = pygame.Surface((width, height))  # Use a surface for the textbox
        self.font = pygame.font.Font(font_path, 24)
        
        self.cursor_visible = True
        self.last_blink_time = pygame.time.get_ticks()
        self.line_height = 27
        self.visible_lines = height // self.line_height
        self.scroll_offset = 0
        self.string = [""]
        self.selection_start = (0, 0)
        self.selection_end = (0, 0)
        self.selecting = False
        self.cursor_pos = 0
        self.i = 0

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse = pygame.mouse.get_pos()
                if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
                    self.selecting = True
                    mouse_x = mouse[0] - self.x
                    mouse_y = mouse[1] - self.y
                    line_index = min(mouse_y // self.line_height, len(self.string) - 1)
                    s = 0
                    index = 0
                    for k in self.string[line_index]:
                        char_width = self.font.size(k)[0]
                        if s + char_width > mouse_x:
                            break
                        s += char_width
                        index += 1
                    if mouse_x < s:
                        index = 0

                    self.i = line_index
                    self.cursor_pos = index
                    self.selection_start = (self.i, self.cursor_pos)
                    self.selection_end = self.selection_start

        elif event.type == pygame.MOUSEMOTION:
            if self.selecting:
                mouse = pygame.mouse.get_pos()
                if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
                    mouse_x = mouse[0] - self.x
                    mouse_y = mouse[1] - self.y
                    line_index = min(mouse_y // self.line_height, len(self.string) - 1)
                    s = 0
                    index = 0
                    for k in self.string[line_index]:
                        char_width = self.font.size(k)[0]
                        if s + char_width > mouse_x:
                            break
                        s += char_width
                        index += 1
                    if mouse_x < s:
                        index = 0

                    self.i = line_index
                    self.cursor_pos = index
                    self.selection_end = (self.i, self.cursor_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.selecting = False
                if self.selection_start[0] > self.selection_end[0] or self.selection_start[1] > self.selection_end[1]:
                    self.selection_start, self.selection_end = self.selection_end, self.selection_start

        elif event.type == pygame.KEYDOWN:
            self.handle_key_event(event)

    def handle_key_event(self, event):
        key = pygame.key.name(event.key)
        if key == "backspace":
            self.handle_backspace()
        elif key == "return":
            self.handle_return()
        elif key == "space":
            self.handle_space()
        elif key == "tab":
            self.handle_tab()
        elif key == "left":
            self.handle_left()
        elif key == "right":
            self.handle_right()
        elif key == "up":
            self.handle_up()
        elif key == "down":
            self.handle_down()
        elif key == "page up":
            self.handle_page_up()
        elif key == "page down":
            self.handle_page_down()
        elif key == "home":
            self.handle_home()
        elif key == "end":
            self.handle_end()
        elif key == "c" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            self.handle_copy()
        elif key == "v" and (pygame.key.get_mods() &(pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            self.handle_paste()
        elif key == "x" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            self.handle_cut()
        elif key == "a" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            self.handle_select_all()
        elif key == "r" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            pass
        elif key == "k" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            pass
        elif key == "e" and (pygame.key.get_mods() & (pygame.KMOD_CTRL | pygame.KMOD_LMETA)):
            pass
        elif len(key) == 1 and key.isalnum() or key in [".", ",", "!", "?", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "{", "}", "\\", "|", ";", ":", "'", "\"", ",", ".", "/", "<", ">", "`", "~"]:
            self.handle_alnum(key)

    def handle_backspace(self):
        if self.selection_start != self.selection_end:
            if self.selection_start[0] == self.selection_end[0]:
                self.string[self.selection_start[0]] = self.string[self.selection_start[0]][:self.selection_start[1]] + self.string[self.selection_start[0]][self.selection_end[1]:]
            else:
                self.string[self.selection_start[0]] = self.string[self.selection_start[0]][:self.selection_start[1]]
                for j in range(self.selection_start[0] + 1, self.selection_end[0]):
                    self.string.pop(self.selection_start[0] + 1)
                if self.selection_start[0] + 1 < len(self.string):
                    self.string[self.selection_start[0]] += self.string[self.selection_start[0] + 1][self.selection_end[1]:]
                    self.string.pop(self.selection_start[0] + 1)

            self.i = self.selection_start[0]
            self.cursor_pos = self.selection_start[1]
            self.selection_start = self.selection_end = (self.i, self.cursor_pos)
        else:
            if self.cursor_pos > 0:
                self.string[self.i] = self.string[self.i][:self.cursor_pos-1] + self.string[self.i][self.cursor_pos:]
                self.cursor_pos -= 1
            elif self.i > 0:
                self.cursor_pos = len(self.string[self.i-1])
                self.i -= 1

    def handle_return(self):
        self.i += 1
        self.string.insert(self.i, "")
        self.cursor_pos = 0

    def handle_space(self):
        self.string[self.i] = self.string[self.i][:self.cursor_pos] + " " + self.string[self.i][self.cursor_pos:]
        self.cursor_pos += 1

    def handle_tab(self):
        self.string[self.i] = self.string[self.i][:self.cursor_pos] + "    " + self.string[self.i][self.cursor_pos:]
        self.cursor_pos += 4

    def handle_left(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1

    def handle_right(self):
        if self.cursor_pos < len(self.string[self.i]):
            self.cursor_pos += 1

    def handle_up(self):
        if self.i > 0:
            self.i -= 1
            self.cursor_pos = min(len(self.string[self.i]), self.cursor_pos)

    def handle_down(self):
        if self.i < len(self.string) - 1:
            self.i += 1
            self.cursor_pos = min(len(self.string[self.i]), self.cursor_pos)

    def handle_page_up(self):
        self.i = max(0, self.i - self.visible_lines)
        self.cursor_pos = min(len(self.string[self.i]), self.cursor_pos)

    def handle_page_down(self):
        self.i = min(len(self.string) - 1, self.i + self.visible_lines)
        self.cursor_pos = min(len(self.string[self.i]), self.cursor_pos)

    def handle_home(self):
        self.cursor_pos = 0

    def handle_end(self):
        self.cursor_pos = len(self.string[self.i])

    def handle_copy(self):
        if self.selection_start != self.selection_end:
            sb = []
            sb.append(self.string[self.selection_start[0]][self.selection_start[1]:])
            for j in range(self.selection_start[0] + 1, self.selection_end[0]):
                sb.append(self.string[j])
            sb.append(self.string[self.selection_end[0]][:self.selection_end[1]])
            pyperclip.copy("\n".join(sb))

    def handle_paste(self):
        pasted_text = pyperclip.paste()
        pasted_lines = pasted_text.splitlines()
        
        if self.selection_start != self.selection_end:
            self.handle_cut()

        self.string[self.i] = self.string[self.i][:self.cursor_pos] + pasted_lines[0]
        rest_of_line = self.string[self.i][self.cursor_pos:]

        for j in range(1, len(pasted_lines)):
            self.i += 1
            self.string.insert(self.i, pasted_lines[j])

        self.string[self.i] += rest_of_line
        self.cursor_pos = len(pasted_lines[-1])

    def handle_cut(self):
        if self.selection_start != self.selection_end:
            sb = []
            sb.append(self.string[self.selection_start[0]][self.selection_start[1]:])
            for j in range(self.selection_start[0] + 1, self.selection_end[0]):
                sb.append(self.string[j])
            sb.append(self.string[self.selection_end[0]][:self.selection_end[1]])
            pyperclip.copy("\n".join(sb))
            self.handle_backspace()

    def handle_select_all(self):
        self.selection_start = (0, 0)
        self.selection_end = (len(self.string) - 1, len(self.string[-1]))

    def handle_alnum(self, key):
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT

        # Dictionary to map Shift + Key to special characters
        shift_map = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', "'": '"', ',': '<', '.': '>', '/': '?',
            '`': '~'
        }

        # Apply shift modifier or caps lock for alphabetic characters
        if key.isalpha():
            if shift_pressed or pygame.key.get_mods() & pygame.KMOD_CAPS:
                key = key.upper()
        # Map numbers and special characters to their Shift variants
        elif shift_pressed and key in shift_map:
            key = shift_map[key]

        # Add the key to the string
        self.string[self.i] = self.string[self.i][:self.cursor_pos] + key + self.string[self.i][self.cursor_pos:]
        self.cursor_pos += 1

    def draw_text(self, surface):
        surface.fill((0, 0, 0))  # Fill the surface with black
        h = 0
        for line_index in range(self.scroll_offset, min(self.scroll_offset + self.visible_lines, len(self.string))):
            el = self.string[line_index]
            if self.selection_start[0] <= line_index <= self.selection_end[0]:
                start_char = self.selection_start[1] if line_index == self.selection_start[0] else 0
                end_char = self.selection_end[1] if line_index == self.selection_end[0] else len(el)
                
                selected_text = el[start_char:end_char]
                selection_width = self.font.size(selected_text)[0]
                selection_x = self.font.size(el[:start_char])[0]
                pygame.draw.rect(surface, (100, 100, 255), (selection_x, h, selection_width, self.line_height))
            surface.blit(self.font.render(el, True, (255, 255, 255)), (0, h))
            h += self.line_height

        current_time = pygame.time.get_ticks()
        if current_time - self.last_blink_time > 500:
            self.cursor_visible = not self.cursor_visible
            self.last_blink_time = current_time    

        if self.cursor_visible:
            cursor_x = self.font.size(self.string[self.i][:self.cursor_pos])[0]
            cursor_y = (self.i - self.scroll_offset) * self.line_height
            pygame.draw.line(surface, (255, 255, 255), (cursor_x, cursor_y), (cursor_x, cursor_y + self.line_height), 2)

    def get_text(self):
        return '\n'.join(self.string)
    
    def set_text(self, new_text):
        self.string = new_text.split("\n")
    
    def clear_text(self):
        self.string = [""]

    def update(self, event):
        self.handle_events(event)

    def draw(self, surface):
        self.draw_text(self.window)
        surface.blit(self.window, (self.x, self.y))
