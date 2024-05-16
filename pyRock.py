# -*- coding:utf-8 -*-
# @Discription:通过pygame获取XBOX手柄的按键，并且通过pyads与twincat进行通讯，将手柄的按键操作发送给twincat
# @Editor:Frank
# @version:1.2
# @:

# 导入pygame，pyads，需要提前安装
import pygame
import pyads
import yaml


def load_config(file_path):
    with open(file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(exc)


# local AmsnetID
config = load_config("config.yaml")
AmsnetID = config.get("AmsnetID")
# default ADS port
PLC_port = 851
# open Port, start plc
try:
    plc = pyads.Connection(AmsnetID, PLC_port)
except BaseException:
    RuntimeError("Not connect to PLC.")
plc.open()

# init pygame
pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# -------- Main Program Loop -----------
while done == False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
    # if event.type == pygame.JOYBUTTONDOWN:
    #    print("Joystick button pressed.")
    # if event.type == pygame.JOYBUTTONUP:
    #    print("Joystick button released.")

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        print("Not find rock.")
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # textPrint.print(screen, "Joystick {}".format(i) )
        # textPrint.indent()

        # Get the name from the OS for the controller/joystick
        # name = joystick.get_name()
        # textPrint.print(screen, "Joystick name: {}".format(name) )

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        # textPrint.print(screen, "Number of axes: {}".format(axes) )
        # textPrint.indent()
        # for i in range(3):
        #     print(joystick.get_axis(i)*128)
        for i in range(axes):
            axis = joystick.get_axis(i) * 128
            print(axis)

            # send axis value to Twincat PLC project
            # print axis value
            if i == 0:
                print("R_x", axis)
                plc.write_by_name("MAIN.stHSHandMaster.valueX", int(axis), pyads.PLCTYPE_INT)
            if i == 1:
                print("R_y", axis)
                plc.write_by_name("MAIN.stHSHandMaster.valueY", int(axis), pyads.PLCTYPE_INT)
            if i == 2:
                print("R_z", axis)
                plc.write_by_name("MAIN.stHSHandMaster.valueZ", int(axis), pyads.PLCTYPE_INT)

        # buttons = joystick.get_numbuttons()
        #
        # for i in range(buttons):
        #     button = joystick.get_button(i)
    clock.tick(20)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
# -------------------------------------------------
