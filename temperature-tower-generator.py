import os

PRUSA_PROFILE_PATH = ""

def produce_stl(min_temp, max_temp, step_temp, fn="temp-tower-test.stl"):
    cmd_template = "openscad -o {} source/tower.scad -D min_temp={} -D max_temp={} -D step_temp={}"
    cmd = cmd_template.format(fn, min_temp, max_temp, step_temp)
    os.system(cmd)

def produce_gcode(fn_in="temp-tower-test.stl", fn_out="temp-tower-test.gcode", fn_bundle="test-config.ini"):
    cmd_template = "prusaslicer -g {} --load {} -o {}"
    cmd = cmd_template.format(fn_in, fn_bundle, fn_out)
    os.system(cmd)

def processs_gcode(temperatures, fn_in="temp-tower-test.gcode", fn_out="final.gcode", fn_bundle="test-config.ini"):
    layer_height = 0
    first_layer_height = 0

    # get layer and first layer height
    with open(fn_bundle, 'r') as f:
        lines = f.readlines()
        layer_height = float([line for line in lines if "layer_height" in line and not "_layer" in line and not "{" in line][0].strip().split(" ")[-1])
        first_layer_height = float([line for line in lines if "first_layer_height" in line][0].strip().split(" ")[-1])

    pass

if __name__=="__main__":
    _min_temp = 200
    _max_temp = 210
    _step_temp = 5
    #produce_stl(_min_temp,_max_temp,_step_temp)
    #produce_gcode()
    temperatures = [i for i in range(_min_temp,_max_temp+1,_step_temp)]
    print(temperatures)
    processs_gcode(temperatures=temperatures)
    # TODO ARG-parse
