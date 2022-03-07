"""
This must be the 7th or 8th game menu program of my life.
It's just as poorly written as the others.
Why do I always do this to myself? Why is it always menus?
"""
import control
import core
import textwrap
import geometry
import settings
import palette
from settings import VIEW_WIDTH, VIEW_HEIGHT
from core import DIRECTIONS, term
from tiles import gfx
from fx import draw_scan_rect

def tag_key(term, key):
    for key_name in DIRECTIONS.keys():
        if key.code == getattr(term, key_name):
            return key_name
        elif key_name == key:
            return key_name

def draw_textbox(rect, paragraphs):
    inner_rect = geometry.grow_y(geometry.grow_x(rect, -2), -1)
    x,y,w,h = inner_rect
    wrapped_lines = []
    for paragraph in paragraphs:
        wrapped_paragraph = textwrap.wrap(paragraph, w)
        wrapped_lines.extend(wrapped_paragraph)
    h_divider = "+-"+"-"*w+"-+"
    with term.location(x,y-1):
        print h_divider
    padded_lines = []
    for line in wrapped_lines:
        padding_amt = w-len(line)
        if padding_amt > 0:
            padding = " "*padding_amt
        else:
            padding = ""
        padded_lines.append("| "+line+padding+" |")
    for blank in range(h-len(padded_lines)):
        padding = " "*w
        padded_lines.append("| "+padding+" |")
    for dy, line in enumerate(padded_lines):
        with term.location(x, y+dy):
            print line
    with term.location(x,y+h+1):
        print h_divider
    
class FloatingMenu:
    def __init__(self, scene, x, y, menu_entries, title = None):
        """
        x,y is coords of topleft
        menu will resize to fit entries
        menu_entries is a list of tuples mapping entry titles to functions
        when an item is selected, the associated function is called
        then the menu closes
        """
        self.cursor_pos = 0
        self.entries = menu_entries
        self.x, self.y = x, y
        self.scene = scene
        self.item_names, self.menu_actions = zip(*menu_entries)
        self.item_names = list(self.item_names)
        self.menu_actions = list(self.menu_actions)
        if title:
            self.entry_width = max([len(e) for e in self.item_names+[title]])
        else:
            self.entry_width = max([len(e) for e in self.item_names])
        self.title = title
    @property
    def selected_entry(self):
        return self.menu_actions[self.cursor_pos]
    @property
    def cursor_loop(self):
        return len(self.entries)
    def update(self, key):
        key_name = None
        if key.name:
            key_name = key.name
        if not key_name:
            key_name = tag_key(term, key)
        if key_name and key_name in DIRECTIONS:
            _, dy = DIRECTIONS[key_name]
            self.cursor_pos += dy
            if self.cursor_pos < 0:
                self.cursor_pos = self.cursor_loop -1
            if self.cursor_pos >= self.cursor_loop:
                self.cursor_pos = 0

        if key_name == "KEY_ENTER" or key == "z" or key_name == "confirm"\
                or key_name == "ability_z":
            if callable(self.selected_entry):
                self.selected_entry()
                return control.DONE
            else:
                return self.selected_entry
    def initial_render(self):
        self.scene.render()
    def render(self):
        x, y = self.x, self.y
        y_offset = 1
        horizontal_divider = "+"+"-"*(self.entry_width+3)+"+"
        m_color = term.bright_white_on_black
        if self.title:
            padding = " "*(self.entry_width - len(self.title)) 
            with term.location(self.x, self.y+y_offset):
                print m_color("| "+self.title+padding+"  |")
                y_offset +=1
            with term.location(self.x, self.y+y_offset):
                print m_color(horizontal_divider)
                y_offset += 1
        with term.location(self.x, self.y):
            print m_color(horizontal_divider)
        for dy, item in enumerate(self.item_names):
            padding = " "*(self.entry_width - len(item))
            with term.location(x, y+dy+y_offset):
                if dy == self.cursor_pos:
                    print(m_color("|>> "+item+padding+"|"))
                else:
                    print(m_color("|   "+item+padding+"|"))
        with term.location(self.x, self.y+len(self.entries)+y_offset):
            print m_color(horizontal_divider)
    def remove(self, menu_entry):
        label, item = menu_entry
        self.entries.remove(menu_entry)
        self.item_names.remove(label)
        self.menu_actions.remove(item)
    def draw(self):
        if hasattr(self.scene, "draw"):
            self.scene.draw()
        else:
            tiles.draw_scene(self.scene)
        top = self.y*settings.TILE_SIZE
        left = self.x*settings.TILE_SIZE
        bounds = (left, top, 12*self.entry_width, 22*len(self.item_names))
        draw_scan_rect(bounds, 3, 25, gap = 4)
        for line, name in enumerate(self.item_names):
            if line != self.cursor_pos:
                sdl_utils.draw_left_text(gfx, left, top + tiles.message_line_height*line,
                        name, color = palette.bright_white)
            else:
                sdl_utils.draw_left_text(gfx, left, top + tiles.message_line_height*line,
                        name, color = palette.bright_white, bg_color = palette.yellow)

TITLE_HEIGHT = 3
VERTICAL_PADDING = 4
class InfoPanelMenu:
    def __init__(self, scene, menu_entries, title = "", info_fields = []):
        """
        x,y is coords of topleft
        menu will resize to fit entries
        menu_entries is a list of tuples mapping entry titles to functions
        when an item is selected, the associated function is called
        then the menu closes
        """
        self.cursor_pos = 0
        self.cursor_loop = len(menu_entries)
        self.entries = menu_entries
        self.x, self.y = (0, 0)
        self.scene = scene
        self.item_names, self.menu_actions = zip(*menu_entries)
        self.entry_width = VIEW_WIDTH/2
        self.title = title
        self.info_fields = info_fields
    def submenu(self, menu_entries):
        num_lines = VIEW_HEIGHT - VERTICAL_PADDING
        lower_bound = max(self.cursor_pos - (num_lines / 2), 0)
        cursor_height = self.cursor_pos - lower_bound + 2
        return FloatingMenu(self, self.entry_width+1, cursor_height,
                menu_entries)
    @property
    def selected_entry(self):
        return self.menu_actions[self.cursor_pos]
    def update(self, key):
        key_name = None
        if key.name:
            key_name = key.name
        if not key_name:
            key_name = tag_key(term, key)
        if key_name and key_name in DIRECTIONS:
            _, dy = DIRECTIONS[key_name]
            self.cursor_pos += dy
            if self.cursor_pos < 0:
                self.cursor_pos = self.cursor_loop -1
            if self.cursor_pos >= self.cursor_loop:
                self.cursor_pos = 0
        if key_name == "KEY_ENTER" or key == "z" or key_name == "confirm"\
                or key_name == "ability_z":
            if callable(self.selected_entry):
                self.selected_entry()
                return control.DONE
            else:
                return self.selected_entry
    def render(self):
        x, y = self.x, self.y
        y_offset = 1
        horizontal_divider = "+"+"-"*(self.entry_width+3)+"+"
        m_color = term.bright_white_on_black
        num_lines = VIEW_HEIGHT - 4
        if self.title:
            padding = " "*(self.entry_width - len(self.title)) 
            with term.location(self.x, self.y+y_offset):
                print m_color("| "+self.title+padding+"  |")
                y_offset += 1
            with term.location(self.x, self.y+y_offset):
                print m_color(horizontal_divider)
                y_offset += 1
        with term.location(self.x, self.y):
            print m_color(horizontal_divider)
        if len(self.item_names) < num_lines:
            display_list = self.item_names
            lower_bound = 0
        else:
            lower_bound = max(self.cursor_pos - (num_lines / 2), 0)
            upper_bound = min(lower_bound + num_lines, len(self.item_names))
            display_list = self.item_names[lower_bound:upper_bound]
        item_padding = tuple([""]*(num_lines - len(display_list)))
        for dy, item in enumerate(tuple(display_list)+item_padding):
            padding = " "*(self.entry_width - len(item))
            with term.location(x, y+dy+y_offset):
                if dy == self.cursor_pos - lower_bound:
                    print(m_color("|>> "+item+padding+"|"))
                else:
                    print(m_color("|   "+item+padding+"|"))
        with term.location(self.entry_width+4, self.y+y_offset-1):
            print m_color(horizontal_divider)
        dy = 0
        field_lines = []
        for field in self.info_fields:
            if field != "":
                text = field.capitalize() + ": "+ str(getattr(self.selected_entry, field))
            else:
                text = ""
            field_lines.append(text)
        draw_textbox((VIEW_WIDTH/2+2, 2, VIEW_WIDTH/2+5, VIEW_HEIGHT-3),
                field_lines)
        with term.location(0, VIEW_HEIGHT-1):
            print horizontal_divider
    def draw(self):
        if hasattr(self.scene, "draw"):
            self.scene.draw()
        else:
            tiles.draw_scene(self.scene)
        top = self.y*settings.TILE_SIZE
        left = self.x*settings.TILE_SIZE
        for line, name in enumerate(self.item_names):
            if line != self.cursor_pos:
                sdl_utils.draw_left_text(gfx, left, top + settings.TILE_SIZE*line,
                        name, color = palette.bright_white)
            else:
                sdl_utils.draw_left_text(gfx, left, top + settings.TILE_SIZE*line,
                        name, color = palette.bright_white, bg_color = palette.yellow)

        field_lines = []
        for field in self.info_fields:
            if field != "":
                text = field.capitalize() + ": "+ str(getattr(self.selected_entry, field))
            else:
                text = ""
            field_lines.append(text)
        info_left = (settings.VIEW_WIDTH/2)*settings.TILE_SIZE
        sdl_utils.draw_paragraph(gfx, info_left, top, 40,
                "\n".join(field_lines), color = palette.bright_white)
