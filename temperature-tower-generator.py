import os, sys, subprocess

def produce_stl(min_temp, max_temp, step_temp, fn="temp-tower-test.stl"):
    tmp_fn = "_tmp_tn.txt"
    cmd_template = "openscad -o {} source/tower.scad -D min_temp={} -D max_temp={} -D step_temp={}"
    cmd = cmd_template.format(fn, min_temp, max_temp, step_temp, tmp_fn)
    os.system(cmd)

if __name__=="__main__":
    produce_stl(200,210,5)
    # TODO ARG-parse
