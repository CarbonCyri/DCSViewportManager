from config import *
from dcs_variables import *
from tkinter import filedialog
from tkinter import *
from KneeboardWriter import write_new_kneeboard
from MonitorConfigBuilder import write_monitor_config
from CockpitScriptsAdjust import write_init_luas
import tkinter.messagebox
import csv
import os
import ctypes.wintypes

to_del = list()
# check for old names in config
for main_item in kneeboard_enabled_airframes:
    if main_item not in dcs_current_airframes:
        to_del.append(main_item)
for main_item in to_del:
    kneeboard_enabled_airframes.remove(main_item)

# Variables for window size and spacing
endrow = round(len(dcs_current_airframes) / 2) + 5
homewidth = 4
savecol = 5
columnsize = 75
rowsize = 25

# Button Colors:
button_green = "#ADFF2F"
button_red = "#D9534F"
button_blue = "#ADD8E6"


# Look for folder in User\Documents, if not existent, create them
CSIDL_PERSONAL = 5       # My Documents
SHGFP_TYPE_CURRENT = 0   # Get current, not default value
buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
user_path = buf.value.replace('\\', '/') + '/DCS ViewportManager/'
user_profile_path = user_path + 'profiles/'
user_template_path = user_path + 'templates/'

if not os.path.isdir(user_path):
    os.mkdir(user_path)
if not os.path.isdir(user_profile_path):
    os.mkdir(user_profile_path)
if not os.path.isdir(user_template_path):
    os.mkdir(user_template_path)

# import .csv-files
# Center Viewport
mainViewport = []
try:
    with open(user_profile_path + "mainViewport.csv", "r", encoding="utf8") as readerfile:
        reader = csv.DictReader(readerfile)
        for line in reader:
            mainViewport.append(line)
except OSError as e:
    mainViewport.append([('name', 'Center'), ('x', '0'), ('y', '0'), ('width', '1920'), ('height', '1080'), ('viewDx', '0'), ('viewDy', '0'), ('aspect', '16/9')])

# Airframe Viewports
viewport_list = []
viewport_airframe.sort()
for vp_airframe in viewport_airframe:
    try:
        with open(user_profile_path + "%s.csv" % vp_airframe, "r", encoding="utf8") as vp_file:
            reader = csv.DictReader(vp_file)
            viewports = []
            for line in reader:
                viewports.append(line)
            viewport_list.append({'airframe': vp_airframe, 'viewports': viewports})
    except OSError as e:
        viewport_list.append({'airframe': vp_airframe, 'viewports': []})


# Application
class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Masterwindow
        self.title("DCS Viewport & Kneeboard Manager")

        # Setup Frame
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        # Create Frame per subpage
        self.frames = {}
        for F in (MainPage, DcsPage, ViewportPage, KneeboardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()


# Main Page
class MainPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        mptitlelabel = Label(self, text="DCS Viewport and Kneeboardposition Manager")
        mptitlelabel.grid(row=0, column=0, columnspan=8, sticky='nesw')

        # DCS-Config Frame
        dcsconfiglabel = Label(self, text="DCS Configuration (Path)")
        dcsconfigbutton = Button(self, text="Setup DCS", command=lambda: controller.show_frame(DcsPage))

        dcsconfiglabel.grid(row=2, column=0, sticky='nesw', columnspan=4)
        dcsconfigbutton.grid(row=3, column=0, sticky='nesw', columnspan=4)

        # Viewport-Config
        viewportconfiglabel = Label(self, text="Viewport Configuration")
        viewportconfigbutton = Button(self, text="Setup Viewports", command=lambda: controller.show_frame(ViewportPage))
        patch_vp = IntVar()

        viewportconfiglabel.grid(row=5, column=0, sticky='nesw', columnspan=4)
        viewportconfigbutton.grid(row=6, column=0, sticky='nesw', columnspan=4)

        # Kneeboard-Config
        kneeboardconfiglabel = Label(self, text="Kneeboard Configuration")
        kneeboardconfigbutton = Button(self, text="Setup Kneeboard", command=lambda: controller.show_frame(KneeboardPage))
        patch_kb = IntVar()

        kneeboardconfiglabel.grid(row=8, column=0, sticky='nesw', columnspan=4)
        kneeboardconfigbutton.grid(row=9, column=0, sticky='nesw', columnspan=4)

        # Layout
        spacer = Label(self, text="", width=10)
        for j in range(7):
            spacer.grid(row=endrow - 1, column=j, sticky='nesw')

        # Patch DCS
        viewportconfigcheckbox = Checkbutton(self, text="Patch Viewports", variable=patch_vp)
        kneeboardconfigcheckbox = Checkbutton(self, text="Patch Kneeboardposition", variable=patch_kb)

        viewportconfigcheckbox.grid(row=endrow-3, column=4, sticky='w', columnspan=4)
        kneeboardconfigcheckbox.grid(row=endrow-2, column=4, sticky='w', columnspan=4)

        patchdcsbutton = Button(self, text="Patch DCS", bg="#ADFF2F", command=lambda p_kb=patch_kb, p_vp=patch_vp: patchdcs_button(p_kb, p_vp))
        patchdcsbutton.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

        # Refresh window
        refresh_button = Button(self, text="Restart Program", bg=button_blue, command=refresh_app)
        refresh_button.grid(row=endrow-1, column=0, sticky="nesw", columnspan=4)

        # Quit Button
        quitbutton = Button(self, text="Quit", bg="#d9534f", command=self.quit)
        quitbutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

        # Layout
        spacer = Label(self, text="", width=10)
        for j in range(7):
            spacer.grid(row=endrow - 1, column=j, sticky='nesw')

        # Create Spacing
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=rowsize)

        if first_run:
            tkinter.messagebox.showinfo("DCS Viewport Manager", "Make sure to adjust the path for your DCS-Game and Saved Games folder. \nPress Setup DCS to adjust them.")


class DcsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Title
        dcslabel = Label(self, text="DCS Variables")
        dcslabel.grid(row=0, column=0, columnspan=8)

        # Textfields + Buttons
        dcspathtitle = Label(self, text="DCS-Game folder:")
        dcspathcurrentlabel = Label(self, text=dcs_Path)
        dcspathsave = Button(self, text="Change folder", padx=5, command=lambda: change_path(dcspathcurrentlabel))

        dcspathtitle.grid(row=2, column=0, sticky='w', columnspan=8)
        dcspathcurrentlabel.grid(row=3, column=0, sticky='w', columnspan=8)
        dcspathsave.grid(row=4, column=0, sticky='nesw', columnspan=4)

        savedgamespathtitle = Label(self, text="Saved Games/DCS folder:")
        savedgamespathcurrentlabel = Label(self, text=savedgames_Path)
        savedgamespathcurrentlabelpathsave = Button(self, text="Change folder", padx=5, command=lambda: change_path(savedgamespathcurrentlabel))

        savedgamespathtitle.grid(row=6, column=0, sticky='w', columnspan=3)
        savedgamespathcurrentlabel.grid(row=7, column=0, sticky='w', columnspan=8)
        savedgamespathcurrentlabelpathsave.grid(row=8, column=0, sticky='nesw', columnspan=4)

        homebutton = Button(self, text="Home", bg=button_blue, command=lambda: controller.show_frame(MainPage))
        homebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

        savechangesbutton = Button(self, text="save changes", bg=button_green, command=lambda: dcs_savechanges(dcspathcurrentlabel['text'], savedgamespathcurrentlabel['text']))
        savechangesbutton.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

        # Layout
        spacer = Label(self, text="", width=10)
        for j in range(7):
            spacer.grid(row=endrow - 1, column=j, sticky='nesw')

        # Create Spacing
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=rowsize)


# Subpage: List of current Viewports
class ViewportPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        viewporttitle = Label(self, text="Viewport-Configuration")
        viewporttitle.grid(row=0, column=0, sticky=W, columnspan=8)
        viewportairframetitle = Label(self, text="Current configured airframes (click to edit):")
        viewportairframetitle.grid(row=1, column=0, sticky=W, columnspan=8)

        viewportmainviewport = Button(self, text="MainViewport", command=mainviewport_pressed)
        viewportmainviewport.grid(row=2, column=0, sticky="NESW", columnspan=4)

        y_pos = 4
        cur_col = 0
        viewport_airframe_buttonlist = {}
        for airframe in viewport_airframe:
            viewport_airframe_buttonlist["v_a_b_%s" % airframe] = Button(self, text=airframe, command=lambda aframe=airframe: vab_pressed(aframe))
            viewport_airframe_buttonlist["v_a_b_%s" % airframe].grid(row=y_pos, column=cur_col, sticky='nesw', columnspan=4)
            if cur_col == 0:
                cur_col = 4
            elif cur_col == 4:
                y_pos += 1
                cur_col = 0

        add_viewport = Button(self, text="Add Airframe", command=lambda: add_airframe(False))
        add_viewport.grid(row=y_pos+2, column=0, sticky="nesw", columnspan=4)

        add_viewport_by_template = Button(self, text="Add Airframe by template", command=lambda: add_airframe(True))
        add_viewport_by_template.grid(row=y_pos + 2, column=4, sticky="nesw", columnspan=4)

        # Layout
        spacer = Label(self, text="", width=10)
        for j in range(7):
            spacer.grid(row=endrow - 1, column=j, sticky='nesw')

        # Create Spacing
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=rowsize)

        viewport_save = Button(self, text="Save Changes", bg=button_green, command=vp_savechanges)
        viewport_save.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

        viewporthomebutton = Button(self, text="Home", bg=button_blue, command=lambda: controller.show_frame(MainPage))
        viewporthomebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)


class KneeboardPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Kneeboard position and size
        kb_label = Label(self, text="Kneeboard position and size")
        kb_x = Label(self, text="x: ")
        kb_y = Label(self, text="y: ")
        kb_w = Label(self, text="width: ")
        kb_h = Label(self, text="height: ")
        kb_x_cur = Label(self, text=kneeboard_size['x'])
        kb_y_cur = Label(self, text=kneeboard_size['y'])
        kb_w_cur = Label(self, text=kneeboard_size['width'])
        kb_h_cur = Label(self, text=kneeboard_size['height'])
        kb_x_entry = Entry(self, width=10)
        kb_y_entry = Entry(self, width=10)
        kb_w_entry = Entry(self, width=10)
        kb_h_entry = Entry(self, width=10)
        kb_x_save = Button(self, text="change", command=lambda key='x', vfield=kb_x_entry, tfield=kb_x_cur: change_value(vfield, tfield, key, None))
        kb_y_save = Button(self, text="change", command=lambda key='y', vfield=kb_y_entry, tfield=kb_y_cur: change_value(vfield, tfield, key, None))
        kb_w_save = Button(self, text="change", command=lambda key='width', vfield=kb_w_entry, tfield=kb_w_cur: change_value(vfield, tfield, key, None))
        kb_h_save = Button(self, text="change", command=lambda key='height', vfield=kb_h_entry, tfield=kb_h_cur: change_value(vfield, tfield, key, None))

        kb_label.grid(row=0, column=0, sticky='nesw', columnspan=4)
        kb_x.grid(row=1, column=0, sticky='e')
        kb_y.grid(row=2, column=0, sticky='e')
        kb_w.grid(row=3, column=0, sticky='e')
        kb_h.grid(row=4, column=0, sticky='e')
        kb_x_cur.grid(row=1, column=1, sticky='e')
        kb_y_cur.grid(row=2, column=1, sticky='e')
        kb_w_cur.grid(row=3, column=1, sticky='e')
        kb_h_cur.grid(row=4, column=1, sticky='e')
        kb_x_entry.grid(row=1, column=2, sticky='nesw')
        kb_y_entry.grid(row=2, column=2, sticky='nesw')
        kb_w_entry.grid(row=3, column=2, sticky='nesw')
        kb_h_entry.grid(row=4, column=2, sticky='nesw')
        kb_x_save.grid(row=1, column=3, sticky='nesw')
        kb_y_save.grid(row=2, column=3, sticky='nesw')
        kb_w_save.grid(row=3, column=3, sticky='nesw')
        kb_h_save.grid(row=4, column=3, sticky='nesw')

        # Enable new Kneeboard for:
        kb_list_label = Label(self, text="Enable new Kneeboard for:")
        kb_list_label.grid(row=0, column=4, columnspan=4, sticky='nesw')

        y_pos = 1
        col = 4
        kb_checkboxlist = {}
        kb_cb_var = {}
        for loopairframe in dcs_current_airframes:
            kb_cb_var[loopairframe] = IntVar()
            kb_checkboxlist["kbc_%s" % loopairframe] = Checkbutton(self, text=loopairframe, variable=kb_cb_var[loopairframe])
            kb_checkboxlist["kbc_%s" % loopairframe].grid(row=y_pos, column=col, sticky='w', columnspan=2)
            if loopairframe in kneeboard_enabled_airframes:
                kb_cb_var[loopairframe].set(1)

            if col == 4:
                col = 6
            else:
                y_pos += 1
                col = 4

        # Check all
        kb_ca_var = IntVar()
        kb_checkall = Checkbutton(self, text="All airframes", variable=kb_ca_var, command=lambda varlist=kb_cb_var: checkall(kb_ca_var, varlist))
        kb_checkall.grid(row=y_pos+2, column=4, sticky='w')

        homebutton = Button(self, text="Home", bg="#add8e6", command=lambda: controller.show_frame(MainPage))
        homebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

        savechangesbutton = Button(self, text="Save changes", bg="#ADFF2F", command=lambda: kb_savechanges([kb_x_cur, kb_y_cur, kb_w_cur, kb_h_cur], kb_cb_var))
        savechangesbutton.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

        # Layout
        spacer = Label(self, text="", width=10)
        for j in range(7):
            spacer.grid(row=endrow - 1, column=j, sticky='nesw')

        # Create Spacing
        col_count, row_count = self.grid_size()
        for col in range(col_count):
            self.grid_columnconfigure(col, minsize=columnsize)
        for row in range(row_count):
            self.grid_rowconfigure(row, minsize=rowsize)


##################################################
##################################################
# Functions:
# General Window fuctions
# refresh app
def refresh_app():
    global app
    app.destroy()
    app = App()

    return


# close window
def close_window(mother, window):
    window.destroy()
    mother.deiconify()

    return


# Update Label with Variable in Entry
def change_value(entryfield, labelfield, key, viewport):
    value = entryfield.get()
    if value == "":
        labelfield.focus()
        entryfield.delete(0, END)
        return
    if key is not None and viewport is not None:
        viewport[key] = value
    labelfield['text'] = value
    labelfield.focus()
    entryfield.delete(0, END)

    return


# change file-path
def change_path(textlabel):
    filename = filedialog.askdirectory()
    if not filename[:-1] == "/":
        filename += "/"
    textlabel['text'] = filename

    return


# special window functions:
# Patch DCS
def patchdcs_button(patch_kb, patch_vp):
    patchstring = ""
    patch_kb_var = patch_kb.get()
    patch_vp_var = patch_vp.get()
    if patch_kb_var == 1:
        write_new_kneeboard(kneeboard_enabled_airframes)
        patchstring += "- Patched Kneeboardpositions\n"
    if patch_vp_var == 1:
        write_init_luas(viewport_list)
        write_monitor_config(mainViewport, viewport_list)
        patchstring += "- Patched Viewports"

    tkinter.messagebox.showinfo("DCS Viewport Manager", "Successfully Patched DCS-Files\n\n%s" % patchstring)

    return


# Save changes to DCS_options
def dcs_savechanges(dcs, savedgames):
    dcs_path_exists = os.path.isdir(dcs)
    sg_path_exists = os.path.isdir(savedgames)

    if dcs_path_exists and sg_path_exists:
        with open("config.py", "r", encoding="utf8") as file:
            data = file.readlines()

        for i in range(len(data)):
            if data[i].startswith("first_run"):
                data[i] = "first_run = False\n"
            elif data[i].startswith("dcs_Path"):
                data[i] = "dcs_Path = r'%s'\n" % dcs
            elif data[i].startswith("savedgames_Path"):
                data[i] = "savedgames_Path = r'%s'\n" % savedgames

        with open("config.py", "w", encoding="utf8") as file:
            file.writelines(data)

        tkinter.messagebox.showinfo("DCS Viewport Manager", "Changes saved:\nDCS: %s\nSaved Games: %s" % (dcs, savedgames))

    else:
        tkinter.messagebox.showinfo("DCS Viewport Manager", "ERROR: Can not find folders. Make sure the entries are valid.")

    return


# save changes to Mainviewport
def mvp_save(values):
    variables = ['x', 'y', 'width', 'height', 'viewDx', 'viewDy', 'aspect']

    for variable in variables:
        mainViewport[0][variable] = values["mvb_%s" % variable]['text']

    tocsv = mainViewport
    keys = tocsv[0].keys()

    with open(user_profile_path + "mainViewport.csv", "w", encoding="utf8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tocsv)

    tkinter.messagebox.showinfo("DCS Viewport Manager", "Mainviewport Saved")

    return


# Save changes made for one airframe
def vp_savechanges():
    successlist = ""
    for airframetwo in viewport_list:
        if airframetwo['viewports']:
            try:
                tocsv = airframetwo['viewports']
                keys = tocsv[0].keys()

                with open(user_profile_path + "%s.csv" % airframetwo['airframe'], "w", encoding="utf8") as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(tocsv)
                successlist += "\n%s" % airframetwo['airframe']
            except PermissionError:
                tkinter.messagebox.showinfo("DCS Viewport Manager", "ERROR: Could not save viewports for %s. Make sure the .csv file is not opened." % airframetwo['airframe'])

    # Make changes to config.py
    va_string = ""
    # create string to write to config
    for i in range(len(viewport_airframe)):
        if i == 0:
            va_string += "viewport_airframe = ['%s'" % viewport_airframe[i]
        else:
            va_string += ", '%s'" % viewport_airframe[i]
    va_string += "]\n"

    # read config
    with open("config.py", "r", encoding="utf8") as file:
        data = file.readlines()

    # replace old array
    for i in range(len(data)):
        if data[i].startswith("viewport_airframe = "):
            data[i] = va_string

    with open("config.py", "w", encoding="utf8") as file:
        file.writelines(data)

    tkinter.messagebox.showinfo("DCS Viewport Manager", "Viewports saved for %s" % successlist)

    return


# Save changes to Kneeboard_options
def kb_savechanges(kneeboard, airframelist):
    kneeboardvar = dict()
    kneeboardvar['x'] = kneeboard[0]['text']
    kneeboardvar['y'] = kneeboard[1]['text']
    kneeboardvar['width'] = kneeboard[2]['text']
    kneeboardvar['height'] = kneeboard[3]['text']

    for loopairframe in dcs_current_airframes:
        boolvar = airframelist[loopairframe].get()
        if boolvar == 1 and loopairframe not in kneeboard_enabled_airframes:
            kneeboard_enabled_airframes.append(loopairframe)
        elif boolvar == 0 and loopairframe in kneeboard_enabled_airframes:
            kneeboard_enabled_airframes.remove(loopairframe)

    # generate strings to write
    kea_string = ""
    kea_string += "kneeboard_enabled_airframes = ['"
    for item in kneeboard_enabled_airframes:
        kea_string += item
        kea_string += "', '"
    kea_string = kea_string[:-3]
    kea_string += "]\n"

    kbp_string = ""
    kbp_string += "kneeboard_size = {'x': %s" % kneeboardvar['x']
    kbp_string += ", 'y': %s" % kneeboardvar['y']
    kbp_string += ", 'width': %s" % kneeboardvar['width']
    kbp_string += ", 'height': %s}\n" % kneeboardvar['height']

    # Read, Modify and Write to config.py
    with open("config.py", "r", encoding="utf8") as file:
        data = file.readlines()

    for i in range(len(data)):
        if data[i].startswith("kneeboard_enabled_airframes = "):
            data[i] = kea_string
        elif data[i].startswith("kneeboard_size = "):
            data[i] = kbp_string

    with open("config.py", "w", encoding="utf8") as file:
        file.writelines(data)

    tkinter.messagebox.showinfo("DCS Viewport Manager", "Saved Changes made to the Kneeboard.\nClick Patch DCS on the Home-Page to apply changes.")

    return


##################################################
# Add module from template
def add_airframe_by_template(module):
    template = list()
    filename = filedialog.askopenfilename(initialdir=user_template_path, title="Pick template.csv", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    try:
        with open(filename, "r", encoding="utf8") as r_file:
            read_data = csv.DictReader(r_file)
            for r_line in read_data:
                template.append(r_line)

        get_screen_information(template, module)

    except OSError:
        tkinter.messagebox.showinfo("DCS Viewport Manager", "Could not read file")

    return


# chose module to add to airframe list
def add_airframe(from_template):
    app.withdraw()
    add_subpage = Tk()
    add_subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=add_subpage: close_window(mother, window))
    add_subpage_frame = Frame(master=add_subpage)
    add_subpage_frame.pack(side="top", fill="both", expand=True)
    add_subpage_frame.grid_rowconfigure(0, weight=1)
    add_subpage_frame.grid_columnconfigure(0, weight=1)

    title_label = Label(add_subpage_frame, text="Add new airframe to viewportlist (click to add)")
    title_label.grid(row=0, column=0, sticky="nesw", columnspan=2)
    add_spacer = Label(add_subpage_frame, text="")
    add_spacer.grid(row=1, column=0)

    addframe_buttonlist = {}
    cur_col = 0
    cur_row = 2
    for item in dcs_current_airframes:
        if item not in viewport_airframe:
            addframe_buttonlist["aaf_%s" % item] = Button(add_subpage_frame, text=item, command=lambda addframe=item: addframetoviewport(addframe, from_template, add_subpage))
            addframe_buttonlist["aaf_%s" % item].grid(row=cur_row, column=cur_col, sticky="nesw")
            if cur_col == 0:
                cur_col = 1
            else:
                cur_col = 0
                cur_row += 1

    # Close Button
    close_button = Button(add_subpage_frame, text="Close", bg="#d9534f", command=lambda mother=app, window=add_subpage: close_window(mother, window))
    close_button.grid(row=endrow, column=0, columnspan=2, sticky="nesw")

    # Layout
    spacer_bot = Label(add_subpage_frame, text="", width=30)
    spacer_bot.grid(row=endrow - 1, column=0, sticky='nesw')
    spacer_bot2 = Label(add_subpage_frame, text="", width=30)
    spacer_bot2.grid(row=endrow - 1, column=1, sticky='nesw')

    # Create Spacing
    add_subpage_frame.grid_columnconfigure(0, minsize=30)
    add_subpage_frame.grid_columnconfigure(1, minsize=30)

    return


# Add module to airframelist
def addframetoviewport(toaddframe, from_template, add_subpage):
    viewport_airframe.append(toaddframe)
    va_string = ""

    # create string to write to config
    for i in range(len(viewport_airframe)):
        if i == 0:
            va_string += "viewport_airframe = ['%s'" % viewport_airframe[i]
        else:
            va_string += ", '%s'" % viewport_airframe[i]
    va_string += "]\n"

    # read config
    with open("config.py", "r", encoding="utf8") as file:
        data = file.readlines()

    # replace old array
    for i in range(len(data)):
        if data[i].startswith("viewport_airframe = "):
            data[i] = va_string

    with open("config.py", "w", encoding="utf8") as file:
        file.writelines(data)

    if not from_template:
        tkinter.messagebox.showinfo("DCS Viewport Manager", "Added %s to airframes in use. Restart the program for this change to appear." % toaddframe)
    else:
        global template_module
        template_module = toaddframe
        add_subpage.destroy()
        app.deiconify()

        add_airframe_by_template(toaddframe)

    return


# remove airframe from viewport_list
def delete_airframe_viewportlist(airframe, window):
    for i in range(len(viewport_list)):
        if viewport_list[i]['airframe'] == airframe:
            del viewport_list[i]
            break
    viewport_airframe.remove(airframe)

    # Rename file to first possible name
    if os.path.isfile(user_profile_path + airframe + ".csv"):
        for i in range(1, 100):
            if not os.path.isfile(user_profile_path + airframe + "_old%s.csv" % i):
                os.rename(user_profile_path + airframe + ".csv", user_profile_path + airframe + "_old%s.csv" % i)
                break

    window.destroy()
    app.deiconify()

    return


# Get viewport_screen information
def get_screen_information(template, module):
    app.withdraw()

    window = Tk()
    window.protocol("WM_DELETE_WINDOW", lambda mother=app: close_window(mother, window))
    window_frame = Frame(master=window)
    window_frame.pack(side="top", fill="both", expand=True)
    window_frame.grid_rowconfigure(0, weight=1)
    window_frame.grid_columnconfigure(0, weight=1)

    # Title
    window_title = Label(window_frame, text="Enter properties of the screen where the viewports should be displayed")
    window_title.grid(row=0, column=0, sticky="nesw", columnspan=4)
    spacer = Label(window_frame, text="")
    spacer.grid(row=2, column=0)

    # Get 2nd screen information
    # hor. position (x)
    resolution_x_label = Label(window_frame, text="2nd screen hor. position (topleft-most pixel):")
    resolution_x_cur = Label(window_frame, text="", width=5)
    resolution_x_entry = Entry(window_frame, text="")
    resolution_x_button = Button(window_frame, takefocus=0, text="Change", command=lambda: change_value(resolution_x_entry, resolution_x_cur, None, None))

    resolution_x_label.grid(row=2, column=0, sticky="nsw")
    resolution_x_cur.grid(row=2, column=1, sticky="e")
    resolution_x_entry.grid(row=2, column=2, sticky="nesw")
    resolution_x_button.grid(row=2, column=3, sticky="nesw")

    # ver. position (y)
    resolution_y_label = Label(window_frame, text="2nd screen ver. position (topleft-most pixel):")
    resolution_y_cur = Label(window_frame, text="", width=5)
    resolution_y_entry = Entry(window_frame, text="")
    resolution_y_button = Button(window_frame, takefocus=0, text="Change", command=lambda: change_value(resolution_y_entry, resolution_y_cur, None, None))

    resolution_y_label.grid(row=3, column=0, sticky="nsw")
    resolution_y_cur.grid(row=3, column=1, sticky="e")
    resolution_y_entry.grid(row=3, column=2, sticky="nesw")
    resolution_y_button.grid(row=3, column=3, sticky="nesw")

    # width
    resolution_width_label = Label(window_frame, text="2nd screen resolution width:")
    resolution_width_cur = Label(window_frame, text="", width=5)
    resolution_width_entry = Entry(window_frame, text="")
    resolution_width_button = Button(window_frame, takefocus=0, text="Change", command=lambda: change_value(resolution_width_entry, resolution_width_cur, None, None))

    resolution_width_label.grid(row=4, column=0, sticky="nsw")
    resolution_width_cur.grid(row=4, column=1, sticky="e")
    resolution_width_entry.grid(row=4, column=2, sticky="nesw")
    resolution_width_button.grid(row=4, column=3, sticky="nesw")

    # height
    resolution_height_label = Label(window_frame, text="2nd screen resolution height:")
    resolution_height_cur = Label(window_frame, text="")
    resolution_height_entry = Entry(window_frame, text="")
    resolution_height_button = Button(window_frame, takefocus=0, text="Change", command=lambda: change_value(resolution_height_entry, resolution_height_cur, None, None))

    resolution_height_label.grid(row=5, column=0, sticky="nsw")
    resolution_height_cur.grid(row=5, column=1, sticky="e")
    resolution_height_entry.grid(row=5, column=2, sticky="nesw")
    resolution_height_button.grid(row=5, column=3, sticky="nesw")

    # Spacer
    spacer = Label(window_frame, text="")
    spacer.grid(row=6, column=0)

    # Close or Save
    close = Button(window_frame, text="Cancel", bg=button_red, command=lambda mother=app: close_window(mother, window))
    close.grid(row=7, column=0, sticky='nesw', columnspan=2)
    save = Button(window_frame, text="Save", bg=button_green, command=lambda win=window: create_screen_information({"x": resolution_x_cur, "y": resolution_y_cur, "width": resolution_width_cur, "height": resolution_height_cur}, template, module, win))
    save.grid(row=7, column=2, sticky="nesw", columnspan=2)

    return


# Write profile using a template
def create_screen_information(screen_config, template, module, window):
    vp_screen = {
        "x": float(screen_config["x"]["text"]),
        "y": float(screen_config["y"]["text"]),
        "width": float(screen_config["width"]["text"]),
        "height": float(screen_config["height"]["text"]),
    }

    final_viewports = list()
    for viewport in template:
        viewport['x'] = int(vp_screen['x'] + int(round(vp_screen['width'] * float(viewport['x']), 0)))
        viewport['y'] = int(vp_screen['y'] + int(round(vp_screen['height'] * float(viewport['y']), 0)))
        viewport['width'] = int(round(vp_screen['width'] * float(viewport['width']), 0))
        viewport['height'] = int(round(vp_screen['height'] * float(viewport['height']), 0))
        final_viewports.append(viewport)

    # write .csv-file
    tocsv = final_viewports
    keys = tocsv[0].keys()

    with open(user_profile_path + "%s.csv" % module, "w", encoding="utf8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tocsv)

    window.destroy()
    app.deiconify()
    tkinter.messagebox.showinfo("DCS Viewport Manager", "Template %s saved." % module)

    return


# Subwindows for template-creation
def create_template(airframe, subpage):
    templatepage = Tk()
    templatepage.protocol("WM_DELETE_WINDOW", lambda mother=subpage, window=templatepage: close_window(mother, window))
    template_frame = Frame(master=templatepage)
    template_frame.pack(side="top", fill="both", expand=True)
    template_frame.grid_rowconfigure(0, weight=1)
    template_frame.grid_columnconfigure(0, weight=1)

    # Title
    template_title = Label(template_frame, text="Create Template based on the profile for: %s" % airframe)
    template_title.grid(row=0, column=0, sticky="nesw", columnspan=4)
    template_spacer = Label(template_frame, text="")
    template_spacer.grid(row=2, column=0)

    # Get 2nd screen information
    # hor. position (x)
    template_resolution_x_label = Label(template_frame, text="2nd screen hor. position (topleft-most pixel):")
    template_resolution_x_cur = Label(template_frame, text="", width=5)
    template_resolution_x_entry = Entry(template_frame, text="")
    template_resolution_x_button = Button(template_frame, takefocus=0, text="Change", command=lambda: change_value(template_resolution_x_entry, template_resolution_x_cur, None, None))

    template_resolution_x_label.grid(row=2, column=0, sticky="nsw")
    template_resolution_x_cur.grid(row=2, column=1, sticky="e")
    template_resolution_x_entry.grid(row=2, column=2, sticky="nesw")
    template_resolution_x_button.grid(row=2, column=3, sticky="nesw")

    # ver. position (y)
    template_resolution_y_label = Label(template_frame, text="2nd screen ver. position (topleft-most pixel):")
    template_resolution_y_cur = Label(template_frame, text="", width=5)
    template_resolution_y_entry = Entry(template_frame, text="")
    template_resolution_y_button = Button(template_frame, takefocus=0, text="Change", command=lambda: change_value(template_resolution_y_entry, template_resolution_y_cur, None, None))

    template_resolution_y_label.grid(row=3, column=0, sticky="nsw")
    template_resolution_y_cur.grid(row=3, column=1, sticky="e")
    template_resolution_y_entry.grid(row=3, column=2, sticky="nesw")
    template_resolution_y_button.grid(row=3, column=3, sticky="nesw")

    # width
    template_resolution_width_label = Label(template_frame, text="2nd screen resolution width:")
    template_resolution_width_cur = Label(template_frame, text="", width=5)
    template_resolution_width_entry = Entry(template_frame, text="")
    template_resolution_width_button = Button(template_frame, takefocus=0, text="Change", command=lambda: change_value(template_resolution_width_entry, template_resolution_width_cur, None, None))

    template_resolution_width_label.grid(row=4, column=0, sticky="nsw")
    template_resolution_width_cur.grid(row=4, column=1, sticky="e")
    template_resolution_width_entry.grid(row=4, column=2, sticky="nesw")
    template_resolution_width_button.grid(row=4, column=3, sticky="nesw")

    # height
    template_resolution_height_label = Label(template_frame, text="2nd screen resolution height:")
    template_resolution_height_cur = Label(template_frame, text="")
    template_resolution_height_entry = Entry(template_frame, text="")
    template_resolution_height_button = Button(template_frame, takefocus=0, text="Change", command=lambda: change_value(template_resolution_height_entry, template_resolution_height_cur, None, None))

    template_resolution_height_label.grid(row=5, column=0, sticky="nsw")
    template_resolution_height_cur.grid(row=5, column=1, sticky="e")
    template_resolution_height_entry.grid(row=5, column=2, sticky="nesw")
    template_resolution_height_button.grid(row=5, column=3, sticky="nesw")

    # Spacer
    template_spacer = Label(template_frame, text="")
    template_spacer.grid(row=6, column=0)

    # Template name
    template_name_label = Label(template_frame, text="Template Name")
    template_name_cur = Label(template_frame, text="")
    template_name_entry = Entry(template_frame, text="")
    template_name_button = Button(template_frame, takefocus=0, text="Change", command=lambda: change_value(template_name_entry, template_name_cur, None, None))

    template_name_label.grid(row=7, column=0, sticky="nsw")
    template_name_cur.grid(row=7, column=1, sticky="e")
    template_name_entry.grid(row=7, column=2, sticky="nesw")
    template_name_button.grid(row=7, column=3, sticky="nesw")

    # Spacer
    template_spacer = Label(template_frame, text="")
    template_spacer.grid(row=8, column=0)

    # Close or Save
    template_close = Button(template_frame, text="Close", bg=button_red, command=lambda mother=subpage, window=templatepage: close_window(mother, window))
    template_close.grid(row=9, column=0, sticky='nesw', columnspan=2)
    template_save = Button(template_frame, text="Save Template", bg=button_green, command=lambda: create_template_final(airframe, {"x": template_resolution_x_cur, "y": template_resolution_y_cur, "width": template_resolution_width_cur, "height": template_resolution_height_cur}, template_name_cur))
    template_save.grid(row=9, column=2, sticky="nesw", columnspan=2)

    return


# Create Template for module_viewports
def create_template_final(dcs_module, screen_config, namefield):
    template_name = namefield["text"]
    module_viewports = list()

    screen_config_val = {
        "x": int(screen_config["x"]["text"]),
        "y": int(screen_config["y"]["text"]),
        "width": int(screen_config["width"]["text"]),
        "height": int(screen_config["height"]["text"])
    }

    for module in viewport_list:
        if module["airframe"] == dcs_module:
            module_viewports = module["viewports"]

    for viewport in module_viewports:
        viewport["x"] = (int(viewport["x"]) - screen_config_val["x"]) / int(screen_config_val["width"])
        viewport["y"] = (int(viewport["y"]) - screen_config_val["y"]) / int(screen_config_val["height"])
        viewport["width"] = int(viewport["width"]) / int(screen_config_val["width"])
        viewport["height"] = int(viewport["height"]) / int(screen_config_val["height"])

    # write .csv-file
    tocsv = module_viewports
    keys = tocsv[0].keys()

    with open(user_template_path + "%s.csv" % template_name, "w", encoding="utf8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(tocsv)

    tkinter.messagebox.showinfo("DCS Viewport Manager", "Template %s saved." % template_name)

    return


# New Frame: MainViweport Page
def mainviewport_pressed():
    app.withdraw()
    subpage = Tk()
    subpage_frame = Frame(master=subpage)
    subpage_frame.pack(side="top", fill="both", expand=True)
    subpage_frame.grid_rowconfigure(0, weight=1)
    subpage_frame.grid_columnconfigure(0, weight=1)
    subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=subpage: close_window(mother, window))

    subpage_title = Label(subpage_frame, text="Viewport-Configuration for the MainViewport (actual game footage)")
    subpage_title.grid(row=0, column=0, sticky=W, columnspan=4)
    subpage_spacer = Label(subpage_frame, text="")
    subpage_spacer.grid(row=1, column=0, sticky=W)

    y_pos = 2
    variables = ['x', 'y', 'width', 'height', 'viewDx', 'viewDy', 'aspect']
    variable_labellist = {}
    variable_valuelist = {}
    variable_entrylist = {}
    variable_savelist = {}

    for variable in variables:
        variable_labellist["mvb_%s" % variable] = Label(subpage_frame, text="%s: " % variable)
        variable_labellist["mvb_%s" % variable].grid(row=y_pos, column=0, sticky="W")

        variable_valuelist["mvb_%s" % variable] = Label(subpage_frame, text=mainViewport[0][variable])
        variable_valuelist["mvb_%s" % variable].grid(row=y_pos, column=1, sticky="W")

        variable_entrylist["mvb_%s" % variable] = Entry(subpage_frame, width=20)
        variable_entrylist["mvb_%s" % variable].grid(row=y_pos, column=2, sticky="NESW")

        variable_savelist["mvb_%s" % variable] = Button(subpage_frame, text="change", command=lambda valuefield=variable_entrylist["mvb_%s" % variable], textfield=variable_valuelist["mvb_%s" % variable]: change_value(valuefield, textfield, None, None))
        variable_savelist["mvb_%s" % variable].grid(row=y_pos, column=3, sticky="NESW")

        y_pos += 1

    subpage_spacer2 = Label(subpage_frame, text="")
    subpage_spacer2.grid(row=y_pos, column=0, sticky=W)

    mviewport_save = Button(subpage_frame, text="Save Changes", bg='#ADFF2F', command=lambda values=variable_valuelist: mvp_save(values))
    mviewport_save.grid(row=y_pos + 1, column=2, sticky='nesw', columnspan=2)

    mviewport_close = Button(subpage_frame, text="Close", bg='#d9534f', command=lambda mother=app, window=subpage: close_window(mother, window))
    mviewport_close.grid(row=y_pos + 1, column=0, sticky='nesw', columnspan=2)

    return


# new Frame to add a viewport to a module
def add_vp(subpage, airframe):
    subpage.withdraw()
    add_vp_window = Tk()
    add_vp_frame = Frame(master=add_vp_window)
    add_vp_frame.pack(side="top", fill="both", expand=True)
    add_vp_frame.grid_rowconfigure(0, weight=1)
    add_vp_frame.grid_columnconfigure(0, weight=1)

    title = Label(add_vp_frame, text="Adding viewport:")
    title.grid(row=0, column=0, sticky=W, columnspan=4)
    spacer = Label(add_vp_frame, text="")
    spacer.grid(row=1, column=0, sticky=W, columnspan=4)

    fields = []

    vp_name_label = Label(add_vp_frame, text="Name:")
    vp_name_cur = Label(add_vp_frame, text="EMPTY")
    vp_name_new = Entry(add_vp_frame, width=10)
    vp_name_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_name_new, textfield=vp_name_cur: change_value(valuefield, textfield, None, None))

    vp_name_label.grid(row=2, column=0, sticky='w')
    vp_name_cur.grid(row=2, column=1, sticky='e')
    vp_name_new.grid(row=2, column=2, sticky='nesw')
    vp_name_save.grid(row=2, column=3, sticky='nesw')
    fields.append(vp_name_cur)

    vp_file_label = Label(add_vp_frame, text="init.lua File:")
    vp_file_cur = Label(add_vp_frame, text="no file selected")
    vp_file_save = Button(add_vp_frame, text="Choose", command=lambda: addviewport_choosefile(vp_file_cur, airframe, None))

    vp_file_label.grid(row=3, column=0, sticky='w')
    vp_file_cur.grid(row=3, column=1, sticky='e')
    vp_file_save.grid(row=3, column=2, sticky='nesw', columnspan=2)
    fields.append(vp_file_cur)

    vp_x_label = Label(add_vp_frame, text="X (hor. pos.):")
    vp_x_cur = Label(add_vp_frame, text="0")
    vp_x_new = Entry(add_vp_frame, width=10)
    vp_x_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_x_new, textfield=vp_x_cur: change_value(valuefield, textfield, None, None))

    vp_x_label.grid(row=4, column=0, sticky='w')
    vp_x_cur.grid(row=4, column=1, sticky='e')
    vp_x_new.grid(row=4, column=2, sticky='nesw')
    vp_x_save.grid(row=4, column=3, sticky='nesw')
    fields.append(vp_x_cur)

    vp_y_label = Label(add_vp_frame, text="Y (ver. pos.):")
    vp_y_cur = Label(add_vp_frame, text="0")
    vp_y_new = Entry(add_vp_frame, width=10)
    vp_y_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_y_new, textfield=vp_y_cur: change_value(valuefield, textfield, None, None))

    vp_y_label.grid(row=5, column=0, sticky='w')
    vp_y_cur.grid(row=5, column=1, sticky='e')
    vp_y_new.grid(row=5, column=2, sticky='w')
    vp_y_save.grid(row=5, column=3, sticky='nesw')
    fields.append(vp_y_cur)

    vp_w_label = Label(add_vp_frame, text="Width:")
    vp_w_cur = Label(add_vp_frame, text="0")
    vp_w_new = Entry(add_vp_frame, width=10)
    vp_w_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_w_new, textfield=vp_w_cur: change_value(valuefield, textfield, None, None))

    vp_w_label.grid(row=6, column=0, sticky='w')
    vp_w_cur.grid(row=6, column=1, sticky='e')
    vp_w_new.grid(row=6, column=2, sticky='nesw')
    vp_w_save.grid(row=6, column=3, sticky='nesw')
    fields.append(vp_w_cur)

    vp_h_label = Label(add_vp_frame, text="Height:")
    vp_h_cur = Label(add_vp_frame, text="0")
    vp_h_new = Entry(add_vp_frame, width=10)
    vp_h_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_h_new, textfield=vp_h_cur: change_value(valuefield, textfield, None, None))

    vp_h_label.grid(row=7, column=0, sticky='w')
    vp_h_cur.grid(row=7, column=1, sticky='e')
    vp_h_new.grid(row=7, column=2, sticky='nesw')
    vp_h_save.grid(row=7, column=3, sticky='nesw')
    fields.append(vp_h_cur)

    spacer2 = Label(add_vp_frame, text="")
    spacer2.grid(row=8, column=0, sticky=W, columnspan=4)

    save = Button(add_vp_frame, text="Save & close", bg=button_green, command=lambda window=add_vp, mother=subpage, af=airframe: addviewport_save(window, af, fields))
    save.grid(row=9, column=0, sticky='nesw', columnspan=4)

    close = Button(add_vp_frame, text="close", bg=button_red, command=lambda window=add_vp, mother=subpage, af=airframe: close_window(window, af))
    close.grid(row=10, column=0, sticky="NESW", columnspan=4)

    return


# chose init-file for a single viewport
def addviewport_choosefile(label, airframe, viewport):
    path = dcs_Path + "Mods/aircraft/"
    if viewport is not None:
        if viewport['filepath'] != "":
            path = dcs_Path + viewport['filepath']
            pathindex = path.rfind("/")
            path = path[0:pathindex + 1]
    else:
        try:
            path = dcs_Path + kneeboard_paths[airframe].replace("device_init.lua", "")
        except OSError:
            path = dcs_Path + "Mods/aircraft/"

    filename = filedialog.askopenfilename(initialdir=path, title="Pick Device_init.lua", filetypes=(("LUA files", "*.lua"), ("all files", "*.*")))

    common_prefix = os.path.commonprefix([filename, dcs_Path])
    if common_prefix == dcs_Path:
        rel_path = os.path.relpath(filename, dcs_Path)
        final_path = rel_path.replace('\\', '/')
    else:
        tkinter.messagebox.showinfo("DCS Viewport Manager", "Invalid Path. Make sure you did setup the corrent DCS-Path on the mainpage and try again")
        return

    if final_path in vp_exceptions:
        tkinter.messagebox.showinfo("DCS Viewport Manager", vp_ecep_hint[final_path])
    label['text'] = final_path

    return


# Save-button Add Viewport Frame
def addviewport_save(window, airframe, fields):
    values = [fields[0]['text'], fields[1]['text'], fields[2]['text'], fields[3]['text'], fields[4]['text'], fields[5]['text']]

    for vpairframe in viewport_list:
        if vpairframe['airframe'] == airframe:
            i = 0
            newviewport = {}
            for fieldvar in ['name', 'filepath', 'x', 'y', 'width', 'height']:
                newviewport[fieldvar] = values[i]
                i += 1
            vpairframe['viewports'].append(newviewport)

    close_window(window, airframe)

    return


# New Frame: List Viewports for one airframe
def vab_pressed(airframe):
    app.withdraw()
    subpage = Tk()
    subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=subpage: close_window(mother, window))
    subpage_frame = Frame(master=subpage)

    subpage_frame.pack(side="top", fill="both", expand=True)
    subpage_frame.grid_rowconfigure(0, weight=1)
    subpage_frame.grid_columnconfigure(0, weight=1)

    subpage_title = Label(subpage_frame, text="Viewport-Configuration for %s" % airframe)
    subpage_title.grid(row=0, column=0, sticky=W, columnspan=3)
    subpage_current_viewports = Label(subpage_frame, text="Current Viewports:")
    subpage_current_viewports.grid(row=1, column=0, sticky=W)

    y_pos = 2
    viewport_buttonlist = {}
    for loopairframe in viewport_list:
        if loopairframe['airframe'] == airframe:
            for viewport in loopairframe['viewports']:
                viewport_buttonlist["v_b_%s" % viewport] = Button(subpage_frame, text=viewport['name'], command=lambda sp=subpage, vport=viewport, af=airframe: vb_pressed(sp, vport, af))
                viewport_buttonlist["v_b_%s" % viewport].grid(row=y_pos, column=0, sticky='nesw')
                y_pos += 1

    viewport_spacer = Label(subpage_frame, text="")
    viewport_spacer.grid(row=y_pos, column=0, sticky='nesw')

    viewport_addnew = Button(subpage_frame, text="Add new viewport", command=lambda sp=subpage, af=airframe: add_vp(sp, af))
    viewport_addnew.grid(row=y_pos+1, column=0, sticky='nesw')

    viewport_spacer2 = Label(subpage_frame, text="")
    viewport_spacer2.grid(row=y_pos+2, column=0, sticky='nesw')

    viewport_createtemplate = Button(subpage_frame, text="Create Template", command=lambda: create_template(airframe, subpage))
    viewport_createtemplate.grid(row=y_pos+3, column=0, sticky='nesw')

    viewport_spacer3 = Label(subpage_frame, text="")
    viewport_spacer3.grid(row=y_pos+4, column=0, sticky='nesw')

    delete_airframe = Button(subpage_frame, text="Delete airframe from list", bg="#FF0000", command=lambda: delete_airframe_viewportlist(airframe, subpage))
    delete_airframe.grid(row=y_pos + 5, column=0, sticky="nesw")

    viewport_close = Button(subpage_frame, text="Close", bg='#d9534f', command=lambda mother=app, window=subpage: close_window(mother, window))
    viewport_close.grid(row=y_pos + 6, column=0, sticky='nesw')

    return


# New Frame: Edit single viewport
def vb_pressed(subpage, viewport, airframe):
    subpage.withdraw()
    edit_vp = Tk()
    edit_vp_frame = Frame(master=edit_vp)
    edit_vp_frame.pack(side="top", fill="both", expand=True)
    edit_vp_frame.grid_rowconfigure(0, weight=1)
    edit_vp_frame.grid_columnconfigure(0, weight=1)
    edit_vp.protocol("WM_DELETE_WINDOW", lambda mother=subpage, window=edit_vp: close_window(mother, window))

    title = Label(edit_vp_frame, text="Editing Viewport %s:" % viewport['name'])
    title.grid(row=0, column=0, sticky=W, columnspan=4)
    spacer = Label(edit_vp_frame, text="")
    spacer.grid(row=2, column=0, sticky=W, columnspan=4)

    vp_file_title = Label(edit_vp_frame, text="init.lua File containing viewport:")
    vp_file_cur = Label(edit_vp_frame, text=viewport['filepath'])
    vp_file_save = Button(edit_vp_frame, text="Choose", command=lambda vp=viewport, label=vp_file_cur: addviewport_choosefile(label, airframe, vp))

    vp_file_title.grid(row=3, column=0, sticky='w', columnspan=4)
    vp_file_cur.grid(row=4, column=0, sticky='w', columnspan=2)
    vp_file_save.grid(row=4, column=2, sticky='nesw', columnspan=2)

    spacer_file = Label(edit_vp_frame, text="")
    spacer_file.grid(row=5, column=0, sticky=W, columnspan=4)

    vp_x_label = Label(edit_vp_frame, text="X (hor. pos.):")
    vp_x_cur = Label(edit_vp_frame, text=viewport['x'])
    vp_x_new = Entry(edit_vp_frame, width=10)
    vp_x_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='x', valuefield=vp_x_new, textfield=vp_x_cur: change_value(valuefield, textfield, key, vp))

    vp_x_label.grid(row=6, column=0, sticky='w')
    vp_x_cur.grid(row=6, column=1, sticky='e')
    vp_x_new.grid(row=6, column=2, sticky='nesw')
    vp_x_save.grid(row=6, column=3, sticky='nesw')

    vp_y_label = Label(edit_vp_frame, text="Y (ver. pos.):")
    vp_y_cur = Label(edit_vp_frame, text=viewport['y'])
    vp_y_new = Entry(edit_vp_frame, width=10)
    vp_y_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='y', valuefield=vp_y_new, textfield=vp_y_cur: change_value(valuefield, textfield, key, vp))

    vp_y_label.grid(row=7, column=0, sticky='w')
    vp_y_cur.grid(row=7, column=1, sticky='e')
    vp_y_new.grid(row=7, column=2, sticky='nesw')
    vp_y_save.grid(row=7, column=3, sticky='nesw')

    vp_w_label = Label(edit_vp_frame, text="Width:")
    vp_w_cur = Label(edit_vp_frame, text=viewport['width'])
    vp_w_new = Entry(edit_vp_frame, width=10)
    vp_w_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='width', valuefield=vp_w_new, textfield=vp_w_cur: change_value(valuefield, textfield, key, vp))

    vp_w_label.grid(row=8, column=0, sticky='w')
    vp_w_cur.grid(row=8, column=1, sticky='e')
    vp_w_new.grid(row=8, column=2, sticky='nesw')
    vp_w_save.grid(row=8, column=3, sticky='nesw')

    vp_h_label = Label(edit_vp_frame, text="Height:")
    vp_h_cur = Label(edit_vp_frame, text=viewport['height'])
    vp_h_new = Entry(edit_vp_frame, width=10)
    vp_h_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='height', valuefield=vp_h_new, textfield=vp_h_cur: change_value(valuefield, textfield, key, vp))

    vp_h_label.grid(row=9, column=0, sticky='w')
    vp_h_cur.grid(row=9, column=1, sticky='e')
    vp_h_new.grid(row=9, column=2, sticky='nesw')
    vp_h_save.grid(row=9, column=3, sticky='nesw')

    spacer2 = Label(edit_vp_frame, text="")
    spacer2.grid(row=10, column=0, sticky=W, columnspan=4)

    save = Button(edit_vp_frame, text="Save & close", bg='#ADFF2F', command=lambda mother=subpage, window=edit_vp: close_window(mother, window))
    save.grid(row=11, column=0, sticky='nesw', columnspan=4)

    del_viewport = Button(edit_vp_frame, text="Delete Viewport", bg="#d9534f", command=lambda mother=subpage, window=edit_vp: delete_viewport(viewport, airframe, window))
    del_viewport.grid(row=12, column=0, sticky="nesw", columnspan=4)

    return


# Delete singgle viewport from module
def delete_viewport(viewport, af, window):
    for i in range(len(viewport_list)):
        if viewport in viewport_list[i]['viewports']:
            viewport_list[i]['viewports'].remove(viewport)
    window.destroy()
    vab_pressed(af)

    return


# Check all checkboxes
def checkall(kb_ca_var, checkboxlist):
    if kb_ca_var.get() == 1:
        for l_airframe in dcs_current_airframes:
            checkboxlist[l_airframe].set(1)
    elif kb_ca_var.get() == 0:
        for l_airframe in dcs_current_airframes:
            checkboxlist[l_airframe].set(0)

    return


##################################################
##################################################
##################################################
# Build App and start mainloop()
app = App()
app.mainloop()

