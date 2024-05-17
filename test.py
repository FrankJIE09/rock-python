import time

axes = 3  # 你的轴数
while True:
    for i in range(axes):
        axis =time.time()* 128
        # 更新要打印的内容
        if i == 0:

            # output = f"R_x: {int(axis)}"
            # plc.write_by_name("MAIN.stHSHandMaster.valueX", int(axis), pyads.PLCTYPE_INT)
        elif i == 1:
            # output = f"R_y: {int(axis)}"
            # plc.write_by_name("MAIN.stHSHandMaster.valueY", int(axis), pyads.PLCTYPE_INT)
        elif i == 2:
            # output = f"R_z: {int(axis)}"
            # plc.write_by_name("MAIN.stHSHandMaster.valueZ", int(axis), pyads.PLCTYPE_INT)
        output =f"R_x: {int(axis)}  R_y: {int(axis)}  R_z: {int(axis)}"
        # 清除之前的内容并打印更新后的内容
        print('\r' + ' ' * 50 + '\r' + output, end='', flush=True)

    # 等待一段时间
    time.sleep(0.1)
