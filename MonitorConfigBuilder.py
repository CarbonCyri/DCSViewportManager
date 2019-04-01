from config import *
from dcs_variables import *


def write_monitor_config(main_viewport, viewport_list):
    config_path = "Config/MonitorSetup/"
    monitorconfig_file = dcs_Path + config_path + "monitor_config_VPM.lua"

    data = []
    data.append("_  = function(p) return p; end;\n")
    data.append("name = _('monitor_config_VPM');\n")
    data.append("Description = 'Monitor-Config created by ViewportManager'\n\n")

    # Main Viewport
    data.append("--########################################\n")
    data.append("-- MAIN VIEWPORT\n")
    data.append("--########################################\n\n")
    data.append("Viewports = \n")
    data.append("{\n")
    data.append("    Center =\n")
    data.append("    {\n")
    data.append("        x = %s;\n" % main_viewport[0]["x"])
    data.append("        y = %s;\n" % main_viewport[0]["y"])
    data.append("        width = %s;\n" % main_viewport[0]["width"])
    data.append("        height = %s;\n" % main_viewport[0]["height"])
    data.append("        viewDx = %s;\n" % main_viewport[0]["viewDx"])
    data.append("        viewDy = %s;\n" % main_viewport[0]["viewDy"])
    data.append("        aspect = %s;\n" % main_viewport[0]["aspect"])
    data.append("    }\n")
    data.append("}\n\n")

    # Viewports per airframe
    for item in viewport_list:
        airframe_name = item['airframe'].replace("-", "_").replace(" ", "_")
        data.append("--########################################\n")
        data.append("-- %s\n" % airframe_name)
        data.append("--########################################\n\n")

        for port in item['viewports']:
            data.append("%s_%s =\n" % (airframe_name, port['name']))
            data.append("{\n")
            data.append("    x = %s;\n" % port['x'])
            data.append("    y = %s;\n" % port['y'])
            data.append("    width = %s;\n" % port['width'])
            data.append("    height = %s;\n" % port['height'])
            data.append("}\n\n")

    data.append("\n\nUIMainView = Viewports.Center")

    with open(monitorconfig_file, 'w', encoding="utf8") as file:
        for line in data:
            file.write(line)

    return
