###########################
# Gamepaths & variables - DO NOT CHANGE
###########################

dcs_current_airframes = [
    "A-10C",
    "A10A",
    "AJS37",
    "AV8BNA",
    "Bf-109K-4",
    "C-101",
    "Christen Eagle II",
    "F-5E",
    "F-86",
    "F14",
    "FA-18C",
    "FW-190D9",
    "Flaming Cliffs",
    "Ka-50",
    "L-39C",
    "M-2000C",
    "MiG-15bis",
    "MIG-21bis",
    "Mi-8MTV2",
    "P-51D",
    "SA342",
    "SpitfireLFMkIX",
    "Uh-1H",
    "Yak-52",
    "MIG19P"
]

vp_handling_path = "Scripts/Aircrafts/_Common/Cockpit/ViewportHandling.lua"
kneeboard_init = "Scripts/Aircrafts/_Common/Cockpit/KNEEBOARD/indicator/init.lua"
kneeboard_declare = "Scripts/Aircrafts/_Common/Cockpit/KNEEBOARD/declare_kneeboard_device.lua"

kneeboard_paths = {
    "A-10C": "Mods/aircraft/A-10C/Cockpit/Scripts/device_init.lua",
    "A10A": "Mods/aircraft/Flaming Cliffs/Cockpit/A10A/device_init.lua",
    "AJS37": "Mods/aircraft/AJS37/Cockpit/scripts/device_init.lua",
    "AV8BNA": "Mods/aircraft/AV8BNA/Cockpit/device_init.lua",
    "Bf-109K-4": "mods/aircraft/Bf-109K-4/Cockpit/Scripts/device_init.lua",
    "C-101CC": "Mods/aircraft/C-101/Cockpit/C-101CC/device_init.lua",
    "C-101EB": "Mods/aircraft/C-101/Cockpit/C-101EB/device_init.lua",
    "Christen Eagle II": "Mods/aircraft/Christen Eagle II/Cockpit/device_init.lua",
    "F-5E": "Mods/aircraft/F-5E/Cockpit/Scripts/device_init.lua",
    "F-86": "Mods/aircraft/F-86/Cockpit/Scripts/device_init.lua",
    "F14": "Mods/aircraft/F14/Cockpit/device_init.lua",
    "FA-18C": "Mods/aircraft/FA-18C/Cockpit/Scripts/device_init.lua",
    "FW-190D9": "Mods/aircraft/FW-190D9/Cockpit/Scripts/device_init.lua",
    "Flaming Cliffs_Right": "Mods/aircraft/Flaming Cliffs/Cockpit/KneeboardRight/device_init.lua",
    "Flaming Cliffs_Left": "Mods/aircraft/Flaming Cliffs/Cockpit/KneeboardLeft/device_init.lua",
    "Ka-50": "Mods/aircraft/Ka-50/Cockpit/Scripts/device_init.lua",
    "L-39C": "Mods/aircraft/L-39C/Cockpit/device_init.lua",
    "M-2000C": "Mods/aircraft/M-2000C/Cockpit/device_init.lua",
    "MiG-15bis": "Mods/aircraft/MiG-15bis/Cockpit/Scripts/device_init.lua",
    "MIG-21bis": "Mods/aircraft/MIG-21bis/Cockpit/device_init.lua",
    "Mi-8MTV2": "Mods/aircraft/Mi-8MTV2/Cockpit/Scripts/device_init.lua",
    "P-51D": "Mods/aircraft/P-51D/Cockpit/Scripts/device_init.lua",
    "SA342": "Mods/aircraft/SA342/Cockpit/device_init.lua",
    "SpitfireLFMkIX": "Mods/aircraft/SpitfireLFMkIX/Cockpit/Scripts/device_init.lua",
    "Uh-1H": "Mods/aircraft/Uh-1H/Cockpit/Scripts/device_init.lua",
    "Yak-52": "Mods/aircraft/Yak-52/Cockpit/Scripts/device_init.lua",
    "MIG19P": "Mods/aircraft/MIG19P/Cockpit/Scripts/device_init.lua"
}

###########################
# Viewport-Exceptions
###########################

vp_exceptions = [
    "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua"
]

vp_ecep_hint = {
    "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua": "The left and right MPCS are stored in the same file.\nTo differentiate between Left and Right MPCD use either left or "
                                                                 "right in the viewportname."
}


