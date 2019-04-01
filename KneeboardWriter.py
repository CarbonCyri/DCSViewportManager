from config import *
from dcs_variables import *
import os


def write_new_kneeboard(kneeboardlist):

    # Create position in new ViewportHandling.lua
    vph_path = dcs_Path + vp_handling_path
    file = open(vph_path, 'r', encoding="utf8")
    vph_data = file.readlines()
    file.close()

    for i in range(len(vph_data)):
        if vph_data[i].startswith('	dedicated_viewport 		  = '):
            vph_data[i] = '	dedicated_viewport 		  = {%s, %s, %s, %s}\n' % (kneeboard_size['x'], kneeboard_size['y'], kneeboard_size['width'], kneeboard_size['height'])

    newfile = vph_path.replace("ViewportHandling.lua", "ViewportHandling_VPM.lua")
    with open(newfile, 'w', encoding="utf8") as file2:
        for line in vph_data:
            file2.write(line)

    # Declare changed ViewportHandling in Kneeboard_init
    kbi_path = dcs_Path + kneeboard_init
    file3 = open(kbi_path, 'r', encoding="utf8")
    kbi_data = file3.readlines()
    file3.close()

    for i in range(len(kbi_data)):
        if kbi_data[i].startswith('dofile(LockOn_Options.common_script_path.."ViewportHandling.lua")'):
            kbi_data[i] = 'dofile(LockOn_Options.common_script_path.."ViewportHandling_VPM.lua")\n'

    newfile = kbi_path.replace("init.lua", "init_VPM.lua")
    with open(newfile, 'w', encoding="utf8") as file4:
        for line in kbi_data:
            file4.write(line)

    # Adjust to new init_VPM.lua
    kbd_path = dcs_Path + kneeboard_declare
    file5 = open(kbd_path, 'r', encoding="utf8")
    kbd_data = file5.readlines()
    file5.close()

    for i in range(len(kbd_data)):
        if kbd_data[i].startswith('local 			init_script = LockOn_Options.common_script_path.."KNEEBOARD/indicator/init'):
            kbd_data[i] = 'local 			init_script = LockOn_Options.common_script_path.."KNEEBOARD/indicator/init_VPM.lua"\n'

    newfile = kbd_path.replace("declare_kneeboard_device.lua", "declare_kneeboard_device_VPM.lua")
    with open(newfile, 'w', encoding="utf8") as file6:
        for line in kbd_data:
            file6.write(line)

    # Adjust selected airframes
    for item in kneeboardlist:
        path = dcs_Path + kneeboard_paths[item]
        exists = os.path.isfile(path)
        if not exists:
            continue

        file7 = open(path, 'r', encoding="utf8")
        data = file7.readlines()
        file7.close()

        for i in range(len(data)):
            if data[i].startswith('dofile(LockOn_Options.common_script_path.."KNEEBOARD/declare_kneeboard_device.lua")'):
                data[i] = 'dofile(LockOn_Options.common_script_path.."KNEEBOARD/declare_kneeboard_device_VPM.lua")\n'

        with open(path, 'w', encoding="utf8") as file8:
            for line in data:
                file8.write(line)

    return
