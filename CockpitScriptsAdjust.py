from config import *
from dcs_variables import *


def write_init_luas(viewport_list):
    for item in viewport_list:
        airframe_name = item['airframe'].replace("-", "_").replace(" ", "_")

        for port in item['viewports']:
            # Read Data
            file = dcs_Path + port['filepath']
            open_file = open(file, 'r', encoding="utf8")
            data = open_file.readlines()
            open_file.close()

            # Find Specific Lines
            if port['filepath'] in vp_exeptions:
                if port['filepath'] == "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua":
                    pos = 0
                    for i in range(len(data)):
                        if data[i].startswith('if monitorpos == 'R' then'):
                            pos = i
                    if pos != 0 and "RIGHT" in port['name'].upper():
                        data[pos + 1] = '	try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])
                    elif pos != 0 and "LEFT" in port['name'].upper():
                        data[pos + 3] = '	try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])

            else:
                found_vp_handling = False
                for i in range(len(data)):
                    if data[i].startswith('dofile(LockOn_Options.common_script_path.."ViewportHandling.lua")'):
                        found_vp_handling = True

                    elif data[i].startswith('try_find_assigned_viewport('):
                        if found_vp_handling:
                            data[i] = 'try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])
                            break
                        else:
                            data[i] = 'dofile(LockOn_Options.common_script_path.."ViewportHandling.lua")\ntry_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])
                            break

            # Write data
            with open(file, 'w', encoding="utf8") as file2:
                for line in data:
                    file2.write(line)

    return
