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

if __name__=="__main__":
    produce_stl(200,210,5)
    produce_gcode()
    # TODO ARG-parse
