###########################
# Gamepaths & variables - DO NOT CHANGE
###########################

dcs_current_airframes = [
    "A-10C",
    "Ka-50",
    "P-51D",
    "Flaming Cliffs",
    "UH-1H",
    "MI-8MTV2",
    "A-10A",
    "F-86",
    "FW-190D9",
    "MIG-21BIS",
    "BF-109K4",
    "C-101",
    "MIG-15BIS",
    "L-39",
    "M-2000C",
    "SA342",
    "F-5E",
    "SpitfireLFMkIX",
    "AJS37",
    "AV8BNA",
    "FA-18C",
    "YAK-52",
    "CE-II",
    "MIG19P",
    "F14"
]

vp_handling_path = "Scripts/Aircrafts/_Common/Cockpit/ViewportHandling.lua"
kneeboard_init = "Scripts/Aircrafts/_Common/Cockpit/KNEEBOARD/indicator/init.lua"
kneeboard_declare = "Scripts/Aircrafts/_Common/Cockpit/KNEEBOARD/declare_kneeboard_device.lua"

kneeboard_paths = {
    "A-10C": "Mods/aircraft/A-10C/Cockpit/Scripts/device_init.lua",
    "Ka-50": "Mods/aircraft/Ka-50/Cockpit/Scripts/device_init.lua",
    "P-51D": "Mods/aircraft/P-51D/Cockpit/Scripts/device_init.lua",
    "Flaming Cliffs": "Mods/aircraft/Flaming Cliffs/Cockpit/KneeboardRight/device_init.lua",
    "Uh-1H": "Mods/aircraft/Uh-1H/Cockpit/Scripts/device_init.lua",
    "Mi-8MTV2": "Mods/aircraft/Mi-8MTV2/Cockpit/Scripts/device_init.lua",
    "A10A": "Mods/aircraft/Flaming Cliffs/Cockpit/A10A/device_init.lua",
    "F-86": "Mods/aircraft/F-86/Cockpit/Scripts/device_init.lua",
        "FW-190D9": "Mods/aircraft/FW-190D9/Cockpit/Scripts/device_init.lua",
        "MIG-21BIS": "Mods/aircraft/MIG-21BIS/Cockpit/Scripts/device_init.lua",
        "BF-109K4": "Mods/aircraft/BF-109K4/Cockpit/Scripts/device_init.lua",
        "C-101": "Mods/aircraft/C-101/Cockpit/Scripts/device_init.lua",
        "MIG-15BIS": "Mods/aircraft/MIG-15BIS/Cockpit/Scripts/device_init.lua",
        "L-39": "Mods/aircraft/L-39/Cockpit/Scripts/device_init.lua",
    "M-2000C": "Mods/aircraft/M-2000C/Cockpit/device_init.lua",
    "SA342": "Mods/aircraft/SA342/Cockpit/device_init.lua",
    "F-5E": "Mods/aircraft/F-5E/Cockpit/Scripts/device_init.lua",
    "SpitfireLFMkIX": "Mods/aircraft/SpitfireLFMkIX/Cockpit/Scripts/device_init.lua",
    "AJS37": "Mods/aircraft/AJS37/Cockpit/scripts/device_init.lua",
    "AV8BNA": "Mods/aircraft/AV8BNA/Cockpit/device_init.lua",
    "FA-18C": "Mods/aircraft/FA-18C/Cockpit/Scripts/device_init.lua",
        "YAK-52": "Mods/aircraft/YAK-52/Cockpit/Scripts/device_init.lua",
        "CE-II": "Mods/aircraft/CE-II/Cockpit/Scripts/device_init.lua",
        "MIG19P": "Mods/aircraft/MIG19P/Cockpit/Scripts/device_init.lua",
    "F14": "Mods/aircraft/F14/Cockpit/device_init.lua"
}

###########################
# Viewport-Exceptions
###########################

vp_exeptions = [
    "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua"
]

vp_ecep_hint = {
    "Mods/aircraft/AV8BNA/Cockpit/MPCD/indicator/MPCD_init.lua": "The left and right MPCS are stored in the same file.\nTo differentiate between Left and Right MPCD use either left or right in the viewportname."
}


