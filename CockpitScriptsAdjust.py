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
            # If in exceptions
            if port['filepath'] in vp_exceptions:
                if port['filepath'] == "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua":
                    pos = 0
                    for i in range(len(data)):
                        if "if monitorpos == 'R' then" in data[i]:
                            pos = i
                    if pos != 0 and "RIGHT" in port['name'].upper():
                        data[pos + 1] = '	try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])
                    elif pos != 0 and "LEFT" in port['name'].upper():
                        data[pos + 3] = '	try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])

            # If normal file
            else:
                vph_line = 0
                vpa_line = 0
                for i in range(len(data)):
                    if 'dofile(LockOn_Options.common_script_path.."ViewportHandling.lua")' in data[i]:
                        vph_line = i
                    elif 'try_find_assigned_viewport(' in data[i]:
                        vpa_line = i

                if vph_line <= 0:
                    data.append('\n\ndofile(LockOn_Options.common_script_path.."ViewportHandling.lua")\n')
                if vpa_line <= 0:
                    data.append('\ntry_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name']))
                else:
                    data[vpa_line] = 'try_find_assigned_viewport("%s_%s")\n' % (airframe_name, port['name'])

            # Write data
            with open(file, 'w', encoding="utf8") as file2:
                for line in data:
                    file2.write(line)

    return
