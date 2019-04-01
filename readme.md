# DCS Viewport Manager (VPM)

**Version:** *0.1*

## WHAT IS DCS Viewport Manager?

This little programm is designed for DCS-Users, who use multiple monitors, especially for those, that use on of their monitors to export different viewports/devices like MFCDs.

The program is divided into four different parts:

1) **Basic configuration** - here you'll need to setup the path to your game-folder aswell as to your saved games\dcs folder.

2) **Vieport-management** - here you are able to select the current airframes inclueded in DCS and for each aircraft you can add multiple viewpors, storing their x- and y-position and their seize. All viewports for one aircraft will be stored and saved in a .csv-file for easy backup and sharing.

3) **Kneeboard-position** - here you can define a position and size for the ingame kneeboard to be displayed. additionally you can select for which aircraft the kneeboard should be displayed at this "new" position instead of the default one.

4) **DCS-filepatche** - this is the final function which allows you to automatically apply the changes made in 2) and 3). This function will:
	a) create a single MonitorConfig.lua file containing all the viewports stored in the .csv-files, seperated by their airframes (Viewportname = AIRFRAME_VIEWPORTNAME)
	b) modifies the DEVICE_init.lua files for each device/viewport created to make their name "unique" (e.g. F18C_RIGHT_MFCD instead of RIGHT_MFCD)
	c) creates modified files for each airframe selected for the kneeboard to be placed at the new position and size
All these changes will pass the Integrety Check and therefore allow to play on multiplayer-servers.


## HOW DO I INSTALL DCS VIEWPORT MANAGER?

This program is written in the coding language called Python. Furthermore it is only compatible with Python 3 and you need to install any Python 3.X version for this to work (like you propably did with Java too).

To install Python 3 
- head to https://www.python.org/downloads/ 
- click on the version you want (newest version at the time of writing is 3.7.3)
- scroll down and download the right version for your computer
	for Windows 64 bit (usually today's default): Windows x86-64 executable installer
	for Windows 32 bit: Windows x86 executable installer
- run the installer and follow the instructions

The next step is to download this program: https://github.com/Alaeya/DCSViewportManager/releases
Download the .zip-archive and extract it into a folder of your choice.


## HOW DO I START THE PROGRAM?

To start the program simply run the RUN VPM.bat - file.
If you have multiple versions of Python installed you may need to adjust the batch-file (rightclick & edit) but I assume if you do, you are familiar with python already.


## HOW DO I USE THIS PROGRAM?

#### Initial setup:
First of all you need to tell the program where it can find all the required files.
Run the program (you will receive a message on your first start / every start when the following initial setup was not done yet) and click on the first button "Setup DCS".
On the following page adjust boths paths for them to fit for your pc. The first is the game-folder, where DCS is installed, the second your saved games\dcs folder (where things like the options-file are stored). To save both paths click on the "save changes" button.


#### Viewport-Configuration:
Click on "Setup Viewports" to enter the viewport-configuration
On the next page you will see the configuration of the MainViewport (main menu & actual game footage) at the top, a list of all airframes currently setup with viewports, a button to add airframes to the list and lastly the home(back) and save changes button.

Click on MainViewport to enter the configuration of your MainViewport and enter your specific variables into the textfields. You need to click change next to the textfield for changes to apply. Click on Save Changes to save the changes made or click on Close to return without saving any changes.

Click on Add Airframe to add a single / multiple airframe to the list. In the following window you can see a list of all airframes inclueded in dcs that are not already on your viewport-list. Click the button to add the airframe to the list. Click close to go back. IMPORTANT: You will not see the added Airframes until you restart the program (this is stil WIP). Before you close the program make sure to press Save Changes on the Viewport-Configuration page to apply changes made!

(After restarting the program after adding new airframes) You will see a list of buttons for each airframe now. Click on a button to enter the viewport-configuration for this airframe. If you do so you will see the list of all configured viewports for this airframe (click the button to make changes to this viewport), a button to add another viewport, a button to delete the whole airframe with all its configured viewports and a Close button to go back to the previous page.
!!!MAKE SURE TO PRESS SAVE CHANGES ON THE VIEWPORT-CONFIGURATION PAGE TO APPLY >ANY< CHANGES MADE.!!!
For more information about the Viewports see below.


#### Kneeboard-Configuration:
Click on "Setup Kneeboard" to enter the Kneeboard-Configuration. At the following page you can edit the position and size of the Kneeboard and select the airframes for which these changes to the kneeboard should be applied. If you select an airframe you don't have installed the program will skip it automatically, feel free to click "All airframes".
Press Save changes to apply any changes made.


#### Patch DCS-files:
On the Home(Main)Page you can select to Patch the configured viewports aswell as the adjusted Kneeboardposition. Select the checkbox and press Patch DCS to patch the gamefiles.
The generated MonitorConfig-file will be called monitor_config_VPM.lua


## KNOWN ISSUES:


## ROADMAP/WISHLIST:

