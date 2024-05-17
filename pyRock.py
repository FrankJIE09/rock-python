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
    for count in range(joystick_count):
        joystick = pygame.joystick.Joystick(count)
        joystick.init()

        # Get the name from the OS for the controller/joystick
        # name = joystick.get_name()
        # textPrint.print(screen, "Joystick name: {}".format(name) )

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        axis_x = joystick.get_axis(0) * 128
        axis_y = joystick.get_axis(1) * 128
        axis_z = joystick.get_axis(2) * 128
        plc.write_by_name("MAIN.stHSHandMaster.valueX", int(axis_x), pyads.PLCTYPE_INT)
        plc.write_by_name("MAIN.stHSHandMaster.valueY", int(axis_y), pyads.PLCTYPE_INT)
        plc.write_by_name("MAIN.stHSHandMaster.valueZ", int(axis_z), pyads.PLCTYPE_INT)

        # 构建要打印的内容
        output_x = f"R_x: {int(axis_x)}"
        output_y = f"R_y: {int(axis_y)}"
        output_z = f"R_z: {int(axis_z)}"

        # 清除之前的内容并打印更新后的内容
        print('\r' + ' ' * 50 + '\r' + output_x + '    ' + output_y + '    ' + output_z, end='', flush=True)
    clock.tick(50)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
# -------------------------------------------------
