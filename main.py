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

endrow = round(len(dcs_current_airframes) / 2) + 5
homewidth = 4
savecol = 5
columnsize = 75
rowsize = 25


# import csv-files
# Center Viewport
mainViewport = []
try:
    reader = csv.DictReader(open("mainViewport.csv", "r", encoding="utf8"))
    for line in reader:
        mainViewport.append(line)
except:
    mainViewport.append([('name', 'Center'), ('x', '0'), ('y', '0'), ('width', '1920'), ('height', '1080'), ('viewDx', '0'), ('viewDy', '0'), ('aspect', '16/9')])

# Airframe Viewports
viewport_list = []
for airframe in viewport_airframe:
    try:
        reader = csv.DictReader(open("%s.csv" % airframe, "r", encoding="utf8"))
        viewports = []
        for line in reader:
            viewports.append(line)
        viewport_list.append({'airframe': airframe, 'viewports': viewports})
    except:
        viewport_list.append({'airframe': airframe, 'viewports': []})


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

        patchdcsbutton = Button(self, text="Patch DCS", bg="#ADFF2F", command=lambda p_kb=patch_kb, p_vp=patch_vp: self.patchdcs_button(p_kb, p_vp))
        patchdcsbutton.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

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

    def patchdcs_button(self, patch_kb, patch_vp):
        patchstring = ""
        patch_kb_var = patch_kb.get()
        patch_vp_var = patch_vp.get()
        if patch_kb_var == 1:
            write_new_kneeboard(kneeboard_enabled_airframes)
            patchstring += "Patched Kneeboardpositions\n"
        if patch_vp_var == 1:
            write_init_luas(viewport_list)
            write_monitor_config(mainViewport, viewport_list)
            patchstring += "Patched Viewports"

        tkinter.messagebox.showinfo("DCS Viewport Manager", "Successfully Patched DCS-Files\n%s" % patchstring)


class DcsPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Title
        dcslabel = Label(self, text="DCS Variables")
        dcslabel.grid(row=0, column=0, columnspan=8)

        # Textfields + Buttons
        dcspathtitle = Label(self, text="DCS-Game folder:")
        dcspathcurrentlabel = Label(self, text=dcs_Path)
        dcspathsave = Button(self, text="Change folder", padx=5, command=lambda: self.change_path(dcspathcurrentlabel))

        dcspathtitle.grid(row=2, column=0, sticky='w', columnspan=8)
        dcspathcurrentlabel.grid(row=3, column=0, sticky='w', columnspan=8)
        dcspathsave.grid(row=4, column=0, sticky='nesw', columnspan=4)

        savedgamespathtitle = Label(self, text="Saved Games/DCS folder:")
        savedgamespathcurrentlabel = Label(self, text=savedgames_Path)
        savedgamespathcurrentlabelpathsave = Button(self, text="Change folder", padx=5, command=lambda: self.change_path(savedgamespathcurrentlabel))

        savedgamespathtitle.grid(row=6, column=0, sticky='w', columnspan=3)
        savedgamespathcurrentlabel.grid(row=7, column=0, sticky='w', columnspan=8)
        savedgamespathcurrentlabelpathsave.grid(row=8, column=0, sticky='nesw', columnspan=4)

        homebutton = Button(self, text="Home", bg="#add8e6", command=lambda: controller.show_frame(MainPage))
        homebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

        savechangesbutton = Button(self, text="save changes", bg='#ADFF2F', command=lambda: self.savechanges(dcspathcurrentlabel['text'], savedgamespathcurrentlabel['text']))
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

    def change_path(self, textlabel):
        filename = filedialog.askdirectory()
        if not filename[:-1] == "/":
            filename += "/"
        textlabel['text'] = filename

    def savechanges(self, dcs, savedgames):
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


# Subpage: List of current Viewports
class ViewportPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        viewporttitle = Label(self, text="Viewport-Configuration")
        viewporttitle.grid(row=0, column=0, sticky=W, columnspan=8)
        viewportairframetitle = Label(self, text="Current configured airframes (click to edit):")
        viewportairframetitle.grid(row=1, column=0, sticky=W, columnspan=8)

        viewportmainviewport = Button(self, text="MainViewport", command=self.mainviewport_pressed)
        viewportmainviewport.grid(row=2, column=0, sticky="NESW", columnspan=4)

        y_pos = 4
        cur_col = 0
        viewport_airframe_buttonlist = {}
        for airframe in viewport_airframe:
            viewport_airframe_buttonlist["v_a_b_%s" % airframe] = Button(self, text=airframe, command=lambda aframe=airframe: self.vab_pressed(aframe))
            viewport_airframe_buttonlist["v_a_b_%s" % airframe].grid(row=y_pos, column=cur_col, sticky='nesw', columnspan=4)
            if cur_col == 0:
                cur_col = 4
            elif cur_col == 4:
                y_pos += 1
                cur_col = 0

        add_viewport = Button(self, text="Add Airframe", command=self.add_airframe)
        add_viewport.grid(row=y_pos+2, column=0, sticky="nesw", columnspan=4)

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

        viewport_save = Button(self, text="Save Changes", bg='#ADFF2F', command=self.save_changes)
        viewport_save.grid(row=endrow, column=4, sticky='nesw', columnspan=4)

        viewporthomebutton = Button(self, text="Home", bg="#add8e6", command=lambda: controller.show_frame(MainPage))
        viewporthomebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

# New Window: Add Airframe
    def add_airframe(self):
        app.withdraw()
        add_subpage = Tk()
        add_subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=add_subpage: self.close_window(mother, window))
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
                addframe_buttonlist["aaf_%s" % item] = Button(add_subpage_frame, text=item, command=lambda addframe=item: self.addframetoviewport(addframe))
                addframe_buttonlist["aaf_%s" % item].grid(row=cur_row, column=cur_col, sticky="nesw")
                if cur_col == 0:
                    cur_col = 1
                else:
                    cur_col = 0
                    cur_row += 1

        # Close Button
        close_button = Button(add_subpage_frame, text="Close", bg="#d9534f", command=lambda mother=app, window=add_subpage: self.close_window(mother, window))
        close_button.grid(row=endrow, column=0, columnspan=2, sticky="nesw")

        # Layout
        spacer_bot = Label(add_subpage_frame, text="", width=30)
        spacer_bot.grid(row=endrow - 1, column=0, sticky='nesw')
        spacer_bot2 = Label(add_subpage_frame, text="", width=30)
        spacer_bot2.grid(row=endrow - 1, column=1, sticky='nesw')

        # Create Spacing
        add_subpage_frame.grid_columnconfigure(0, minsize=30)
        add_subpage_frame.grid_columnconfigure(1, minsize=30)

    def addframetoviewport(self, toaddframe):
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

        tkinter.messagebox.showinfo("DCS Viewport Manager", "Added %s to airframes in use. Restart the program for this change to appear" % toaddframe)


# New Frame: MainViweport Page
    def mainviewport_pressed(self):
        app.withdraw()
        subpage = Tk()
        subpage_frame = Frame(master=subpage)
        subpage_frame.pack(side="top", fill="both", expand=True)
        subpage_frame.grid_rowconfigure(0, weight=1)
        subpage_frame.grid_columnconfigure(0, weight=1)
        subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=subpage: self.close_window(mother, window))

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

            variable_savelist["mvb_%s" % variable] = Button(subpage_frame, text="change", command=lambda valuefield=variable_entrylist["mvb_%s" % variable], textfield=variable_valuelist["mvb_%s" % variable]: self.change_mvp_value(valuefield, textfield))
            variable_savelist["mvb_%s" % variable].grid(row=y_pos, column=3, sticky="NESW")

            y_pos += 1

        subpage_spacer2 = Label(subpage_frame, text="")
        subpage_spacer2.grid(row=y_pos, column=0, sticky=W)

        mviewport_save = Button(subpage_frame, text="Save Changes", bg='#ADFF2F', command=lambda values=variable_valuelist: self.save_mvp(values))
        mviewport_save.grid(row=y_pos + 1, column=2, sticky='nesw', columnspan=2)

        mviewport_close = Button(subpage_frame, text="Close", bg='#d9534f', command=lambda mother=app, window=subpage: self.close_window(mother, window))
        mviewport_close.grid(row=y_pos + 1, column=0, sticky='nesw', columnspan=2)

    def change_mvp_value(self, valuefield, textfield):
        value = valuefield.get()
        textfield['text'] = value
        textfield.focus()
        valuefield.delete(0, END)

    def save_mvp(self, values):
        variables = ['x', 'y', 'width', 'height', 'viewDx', 'viewDy', 'aspect']

        for variable in variables:
            mainViewport[0][variable] = values["mvb_%s" % variable]['text']

        tocsv = mainViewport
        keys = tocsv[0].keys()

        with open("mainViewport.csv", "w", encoding="utf8") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(tocsv)

        tkinter.messagebox.showinfo("DCS Viewport Manager", "Mainviewport Saved")
        self.focus_force()

# New Frame: List Viewports for one airframe
    def vab_pressed(self, airframe):
        app.withdraw()
        subpage = Tk()
        subpage.protocol("WM_DELETE_WINDOW", lambda mother=app, window=subpage: self.close_window(mother, window))
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
                    viewport_buttonlist["v_b_%s" % viewport] = Button(subpage_frame, text=viewport['name'], command=lambda sp=subpage, vport=viewport, af=airframe: self.vb_pressed(sp, vport, af))
                    viewport_buttonlist["v_b_%s" % viewport].grid(row=y_pos, column=0, sticky='nesw')
                    y_pos += 1

        viewport_spacer = Label(subpage_frame, text="")
        viewport_spacer.grid(row=y_pos, column=0, sticky='nesw')

        viewport_addnew = Button(subpage_frame, text="Add new viewport", command=lambda sp=subpage, af=airframe: self.add_vp(sp, af))
        viewport_addnew.grid(row=y_pos+1, column=0, sticky='nesw')

        viewport_spacer2 = Label(subpage_frame, text="")
        viewport_spacer2.grid(row=y_pos+2, column=0, sticky='nesw')

        delete_airframe = Button(subpage_frame, text="Delete airframe from list", bg="#FF0000", command=lambda: self.delete_airframe_viewportlist(airframe, subpage))
        delete_airframe.grid(row=y_pos + 4, column=0, sticky="nesw")

        viewport_close = Button(subpage_frame, text="Close", bg='#d9534f', command=lambda mother=app, window=subpage: self.close_window(mother, window))
        viewport_close.grid(row=y_pos + 5, column=0, sticky='nesw')

    def delete_airframe_viewportlist(self, airframe, window):
        for i in range(len(viewport_list)):
            if viewport_list[i]['airframe'] == airframe:
                del viewport_list[i]
                break

        viewport_airframe.remove(airframe)

        window.destroy()
        app.deiconify()


# New Frame: Edit single viewport
    def vb_pressed(self, subpage, viewport, af):
        subpage.withdraw()
        edit_vp = Tk()
        edit_vp_frame = Frame(master=edit_vp)
        edit_vp_frame.pack(side="top", fill="both", expand=True)
        edit_vp_frame.grid_rowconfigure(0, weight=1)
        edit_vp_frame.grid_columnconfigure(0, weight=1)
        edit_vp.protocol("WM_DELETE_WINDOW", lambda mother=subpage, window=edit_vp: self.close_window(mother, window))

        title = Label(edit_vp_frame, text="Editing Viewport %s:" % viewport['name'])
        title.grid(row=0, column=0, sticky=W, columnspan=4)
        spacer = Label(edit_vp_frame, text="")
        spacer.grid(row=2, column=0, sticky=W, columnspan=4)

        vp_file_title = Label(edit_vp_frame, text="init.lua File containing viewport:")
        vp_file_cur = Label(edit_vp_frame, text=viewport['filepath'])
        vp_file_save = Button(edit_vp_frame, text="Choose", command=lambda vp=viewport, label=vp_file_cur: self.chose_vp_file(vp, label))

        vp_file_title.grid(row=3, column=0, sticky='w', columnspan=4)
        vp_file_cur.grid(row=4, column=0, sticky='w', columnspan=2)
        vp_file_save.grid(row=4, column=2, sticky='nesw', columnspan=2)

        spacer_file = Label(edit_vp_frame, text="")
        spacer_file.grid(row=5, column=0, sticky=W, columnspan=4)

        vp_x_label = Label(edit_vp_frame, text="X (hor. pos.):")
        vp_x_cur = Label(edit_vp_frame, text=viewport['x'])
        vp_x_new = Entry(edit_vp_frame, width=10)
        vp_x_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='x', valuefield=vp_x_new, textfield=vp_x_cur: self.change_vp_value(vp, key, valuefield, textfield))

        vp_x_label.grid(row=6, column=0, sticky='w')
        vp_x_cur.grid(row=6, column=1, sticky='e')
        vp_x_new.grid(row=6, column=2, sticky='nesw')
        vp_x_save.grid(row=6, column=3, sticky='nesw')

        vp_y_label = Label(edit_vp_frame, text="Y (ver. pos.):")
        vp_y_cur = Label(edit_vp_frame, text=viewport['y'])
        vp_y_new = Entry(edit_vp_frame, width=10)
        vp_y_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='y', valuefield=vp_y_new, textfield=vp_y_cur: self.change_vp_value(vp, key, valuefield, textfield))

        vp_y_label.grid(row=7, column=0, sticky='w')
        vp_y_cur.grid(row=7, column=1, sticky='e')
        vp_y_new.grid(row=7, column=2, sticky='nesw')
        vp_y_save.grid(row=7, column=3, sticky='nesw')

        vp_w_label = Label(edit_vp_frame, text="Width:")
        vp_w_cur = Label(edit_vp_frame, text=viewport['width'])
        vp_w_new = Entry(edit_vp_frame, width=10)
        vp_w_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='width', valuefield=vp_w_new, textfield=vp_w_cur: self.change_vp_value(vp, key, valuefield, textfield))

        vp_w_label.grid(row=8, column=0, sticky='w')
        vp_w_cur.grid(row=8, column=1, sticky='e')
        vp_w_new.grid(row=8, column=2, sticky='nesw')
        vp_w_save.grid(row=8, column=3, sticky='nesw')

        vp_h_label = Label(edit_vp_frame, text="Height:")
        vp_h_cur = Label(edit_vp_frame, text=viewport['height'])
        vp_h_new = Entry(edit_vp_frame, width=10)
        vp_h_save = Button(edit_vp_frame, text="Change", takefocus=0, command=lambda vp=viewport, key='height', valuefield=vp_h_new, textfield=vp_h_cur: self.change_vp_value(vp, key, valuefield, textfield))

        vp_h_label.grid(row=9, column=0, sticky='w')
        vp_h_cur.grid(row=9, column=1, sticky='e')
        vp_h_new.grid(row=9, column=2, sticky='nesw')
        vp_h_save.grid(row=9, column=3, sticky='nesw')

        spacer2 = Label(edit_vp_frame, text="")
        spacer2.grid(row=10, column=0, sticky=W, columnspan=4)

        save = Button(edit_vp_frame, text="Save & close", bg='#ADFF2F', command=lambda mother=subpage, window=edit_vp: self.close_window(mother, window))
        save.grid(row=11, column=0, sticky='nesw', columnspan=4)

        delete_viewport = Button(edit_vp_frame, text="Delete Viewport", bg="#d9534f", command=lambda mother=subpage, window=edit_vp: self.delete_viewport(viewport, af, window))
        delete_viewport.grid(row=12, column=0, sticky="nesw", columnspan=4)

    def delete_viewport(self, viewport, af, window):
        for i in range(len(viewport_list)):
            if viewport in viewport_list[i]['viewports']:
                viewport_list[i]['viewports'].remove(viewport)
        window.destroy()
        self.vab_pressed(af)

    def close_window(self, mother, window):
        window.destroy()
        mother.deiconify()

    def change_vp_value(self, viewport, key, valuefield, textfield):
        value = valuefield.get()
        if value == "":
            textfield.focus()
            valuefield.delete(0, END)
            return
        viewport[key] = value
        textfield['text'] = value
        textfield.focus()
        valuefield.delete(0, END)

    def chose_vp_file(self, viewport, label):
        if viewport['filepath'] != "":
            path = dcs_Path + viewport['filepath']
            pathindex = path.rfind("/")
            path = path[0:pathindex+1]
        else:
            path = dcs_Path

        filename = filedialog.askopenfilename(initialdir=path, title="Pick Device_init.lua", filetypes=(("LUA files", "*.lua"), ("all files", "*.*")))

        common_prefix = os.path.commonprefix([filename, dcs_Path])
        if common_prefix == dcs_Path:
            rel_path = os.path.relpath(filename, dcs_Path)
            final_path = rel_path.replace('\\', '/')
        else:
            tkinter.messagebox.showinfo("DCS Viewport Manager", "Invalid Path. Make sure you did setup the corrent DCS-Path on the mainpage and try again")
            return

        if final_path in vp_exeptions:
            tkinter.messagebox.showinfo("DCS Viewport Manager", vp_ecep_hint[final_path])

        viewport['filepath'] = final_path
        label['text'] = final_path

# Save changes made for one airframe
    def save_changes(self):
        successlist = ""
        for airframetwo in viewport_list:
            if airframetwo['viewports']:
                try:
                    tocsv = airframetwo['viewports']
                    keys = tocsv[0].keys()

                    with open("%s.csv" % airframetwo['airframe'], "w", encoding="utf8") as output_file:
                        dict_writer = csv.DictWriter(output_file, keys)
                        dict_writer.writeheader()
                        dict_writer.writerows(tocsv)
                    successlist += "%s, " % airframetwo['airframe']
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

# New Frame: Create new viewport
    def add_vp(self, subpage, airframe):
        subpage.withdraw()
        add_vp = Tk()
        add_vp_frame = Frame(master=add_vp)
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
        vp_name_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_name_new, textfield=vp_name_cur: self.addviewport_change(valuefield, textfield))

        vp_name_label.grid(row=2, column=0, sticky='w')
        vp_name_cur.grid(row=2, column=1, sticky='e')
        vp_name_new.grid(row=2, column=2, sticky='nesw')
        vp_name_save.grid(row=2, column=3, sticky='nesw')
        fields.append(vp_name_cur)

        vp_file_label = Label(add_vp_frame, text="init.lua File:")
        vp_file_cur = Label(add_vp_frame, text="no file selected")
        vp_file_save = Button(add_vp_frame, text="Choose", command=lambda: self.addviewport_choosefile(vp_file_cur, airframe))

        vp_file_label.grid(row=3, column=0, sticky='w')
        vp_file_cur.grid(row=3, column=1, sticky='e')
        vp_file_save.grid(row=3, column=2, sticky='nesw', columnspan=2)
        fields.append(vp_file_cur)

        vp_x_label = Label(add_vp_frame, text="X (hor. pos.):")
        vp_x_cur = Label(add_vp_frame, text="0")
        vp_x_new = Entry(add_vp_frame, width=10)
        vp_x_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_x_new, textfield=vp_x_cur: self.addviewport_change(valuefield, textfield))

        vp_x_label.grid(row=4, column=0, sticky='w')
        vp_x_cur.grid(row=4, column=1, sticky='e')
        vp_x_new.grid(row=4, column=2, sticky='nesw')
        vp_x_save.grid(row=4, column=3, sticky='nesw')
        fields.append(vp_x_cur)

        vp_y_label = Label(add_vp_frame, text="Y (ver. pos.):")
        vp_y_cur = Label(add_vp_frame, text="0")
        vp_y_new = Entry(add_vp_frame, width=10)
        vp_y_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_y_new, textfield=vp_y_cur: self.addviewport_change(valuefield, textfield))

        vp_y_label.grid(row=5, column=0, sticky='w')
        vp_y_cur.grid(row=5, column=1, sticky='e')
        vp_y_new.grid(row=5, column=2, sticky='w')
        vp_y_save.grid(row=5, column=3, sticky='nesw')
        fields.append(vp_y_cur)

        vp_w_label = Label(add_vp_frame, text="Width:")
        vp_w_cur = Label(add_vp_frame, text="0")
        vp_w_new = Entry(add_vp_frame, width=10)
        vp_w_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_w_new, textfield=vp_w_cur: self.addviewport_change(valuefield, textfield))

        vp_w_label.grid(row=6, column=0, sticky='w')
        vp_w_cur.grid(row=6, column=1, sticky='e')
        vp_w_new.grid(row=6, column=2, sticky='nesw')
        vp_w_save.grid(row=6, column=3, sticky='nesw')
        fields.append(vp_w_cur)

        vp_h_label = Label(add_vp_frame, text="Height:")
        vp_h_cur = Label(add_vp_frame, text="0")
        vp_h_new = Entry(add_vp_frame, width=10)
        vp_h_save = Button(add_vp_frame, text="Change", takefocus=0, command=lambda valuefield=vp_h_new, textfield=vp_h_cur: self.addviewport_change(valuefield, textfield))

        vp_h_label.grid(row=7, column=0, sticky='w')
        vp_h_cur.grid(row=7, column=1, sticky='e')
        vp_h_new.grid(row=7, column=2, sticky='nesw')
        vp_h_save.grid(row=7, column=3, sticky='nesw')
        fields.append(vp_h_cur)

        spacer2 = Label(add_vp_frame, text="")
        spacer2.grid(row=8, column=0, sticky=W, columnspan=4)

        save = Button(add_vp_frame, text="Save & close", bg='#ADFF2F', command=lambda window=add_vp, mother=subpage, af=airframe: self.addviewport_save(window, af, fields))
        save.grid(row=9, column=0, sticky='nesw', columnspan=4)

        close = Button(add_vp_frame, text="close", bg='#d9534f', command=lambda window=add_vp, mother=subpage, af=airframe: self.addviewport_close(window, af))
        close.grid(row=10, column=0, sticky="NESW", columnspan=4)

    def addviewport_change(self, valuefield, textfield):
            value = valuefield.get()
            if value == "":
                textfield.focus()
                valuefield.delete(0, END)
                return
            textfield['text'] = value
            textfield.focus()
            valuefield.delete(0, END)

    def addviewport_choosefile(self, label, airframe):
        try:
            path = dcs_Path + kneeboard_paths[airframe].replace("device_init.lua", "")
        except:
            path = dcs_Path + "Mods/aircraft/"

        filename = filedialog.askopenfilename(initialdir=path, title="Pick Device_init.lua", filetypes=(("LUA files", "*.lua"), ("all files", "*.*")))

        common_prefix = os.path.commonprefix([filename, dcs_Path])
        if common_prefix == dcs_Path:
            rel_path = os.path.relpath(filename, dcs_Path)
            final_path = rel_path.replace('\\', '/')
        else:
            tkinter.messagebox.showinfo("DCS Viewport Manager", "Invalid Path. Make sure you did setup the corrent DCS-Path on the mainpage and try again")
            return

        if final_path in vp_exeptions:
            tkinter.messagebox.showinfo("DCS Viewport Manager", vp_ecep_hint[final_path])
        label['text'] = final_path

    def addviewport_save(self, window, airframe, fields):
        values = [fields[0]['text'], fields[1]['text'], fields[2]['text'], fields[3]['text'], fields[4]['text'], fields[5]['text']]

        for vpairframe in viewport_list:
            if vpairframe['airframe'] == airframe:
                i = 0
                newviewport = {}
                for fieldvar in ['name', 'filepath', 'x', 'y', 'width', 'height']:
                    newviewport[fieldvar] = values[i]
                    i += 1
                vpairframe['viewports'].append(newviewport)

        self.addviewport_close(window, airframe)

    def addviewport_close(self, window, airframe):
        window.destroy()
        self.vab_pressed(airframe)


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
        kb_x_save = Button(self, text="change", command=lambda key='x', vfield=kb_x_entry, tfield=kb_x_cur: self.change_kb_value(key, vfield, tfield))
        kb_y_save = Button(self, text="change", command=lambda key='y', vfield=kb_y_entry, tfield=kb_y_cur: self.change_kb_value(key, vfield, tfield))
        kb_w_save = Button(self, text="change", command=lambda key='width', vfield=kb_w_entry, tfield=kb_w_cur: self.change_kb_value(key, vfield, tfield))
        kb_h_save = Button(self, text="change", command=lambda key='height', vfield=kb_h_entry, tfield=kb_h_cur: self.change_kb_value(key, vfield, tfield))

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
        kb_checkall = Checkbutton(self, text="All airframes", variable=kb_ca_var, command=lambda varlist=kb_cb_var: self.checkall(kb_ca_var, varlist))
        kb_checkall.grid(row=y_pos+2, column=4, sticky='w')

        homebutton = Button(self, text="Home", bg="#add8e6", command=lambda: controller.show_frame(MainPage))
        homebutton.grid(row=endrow, column=0, sticky='nesw', columnspan=4)

        savechangesbutton = Button(self, text="Save changes", bg="#ADFF2F", command=lambda kneeboard=[kb_x_cur, kb_y_cur, kb_w_cur, kb_h_cur]: self.savechanges(kneeboard, kb_cb_var))
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

    def checkall(self, kb_ca_var, checkboxlist):
        if kb_ca_var.get() == 1:
            for l_airframe in dcs_current_airframes:
                checkboxlist[l_airframe].set(1)
        elif kb_ca_var.get() == 0:
            for l_airframe in dcs_current_airframes:
                checkboxlist[l_airframe].set(0)

    def change_kb_value(self, key, valuefield, textfield):
        value = valuefield.get()
        kneeboard_size[key] = value
        textfield['text'] = value
        textfield.focus()
        valuefield.delete(0, END)

    def savechanges(self, kneeboard, airframelist):
        kneeboardvar = {}
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


app = App()
app.mainloop()


