import os, sys

import argparse

# TODO: add constants/templates for the filenames

def get_value_at_line(l):
    return l[0].strip().split(" = ")[-1]

def extract_data_from_ini(fn_config):

    with open(fn_config, 'r') as f:
        bundle_lines = f.readlines()
        layer_height = float(get_value_at_line([line for line in bundle_lines if "layer_height" in line and not "_layer" in line and not "{" in line]))
        first_layer_height = float(get_value_at_line([line for line in bundle_lines if "first_layer_height" in line]))
        filament_name = get_value_at_line([line for line in bundle_lines if "filament_settings_id" in line])
    
    return first_layer_height, layer_height, filament_name

def produce_stl(min_temp, max_temp, step_temp, fn="temp-tower-test.stl"):
    cmd_template = "openscad -o {} source/tower.scad -D min_temp={} -D max_temp={} -D step_temp={}"
    cmd = cmd_template.format(fn, min_temp, max_temp, step_temp)
    os.system(cmd)

def produce_gcode(fn_in="temp-tower-test.stl", fn_out="temp-tower-test.gcode", fn_config="test-config.ini"):
    cmd_template = "prusaslicer -g {} --load {} -o {}"
    cmd = cmd_template.format(fn_in, fn_config, fn_out)
    os.system(cmd)

def processs_gcode(first_layer_height, layer_height, temperatures, fn_in="temp-tower-test.gcode", fn_out="final.gcode"):
    
    # TODO: make this constant/autoloadable
    base_height = 1
    floor_height = 10
    
    # read gcode the gcode
    gcode_lines = ""
    with open(fn_in, 'r') as f:
        gcode_lines = "".join(f.readlines())
    
    # get total number of layers
    n_layers = gcode_lines.count("\n;AFTER_LAYER_CHANGE")
    # generarate layers based on the first layer height and layer height
    gcode_layers = [first_layer_height+i*layer_height for i in range(n_layers)]

    # get the precise layers for temperature change
    n_floors = len(temperatures)

    # identifying the true layer where the new layers start
    new_floor_layers = [base_height+i*floor_height for i in range(n_floors)]
    temp_change_at = []
    for fl in new_floor_layers:
        diff = gcode_layers[-1]
        idx = None
        # finding the closes layer
        for l_idx in range(len(gcode_layers)):
            l = gcode_layers[l_idx]
            if abs(fl-l) < diff:
                diff = abs(fl-l)
                idx = l_idx
        # temperature is changed on the next layer
        temp_change_at.append(idx+1)
    
    # injecting temperature change
    search_template = ";LAYER_CHANGE\n;Z:{:.3f}"
    for i in range(n_floors):
        l_idx = temp_change_at[i]
        lc = gcode_layers[l_idx]
        temp = temperatures[i]
        search_string = search_template.format(lc).strip("0")
        new_string = search_string + "\nM104 S{}".format(temp)
        # replacing and updating gcode
        gcode_lines = gcode_lines.replace(search_string,new_string)
    
    # updating the gcode
    with open(fn_out,'w') as f:
        f.write(gcode_lines)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            prog = '{}'.format(__file__),
            description = 'Creates gcode for temperature tower to select an optimal printing temperature. The temperature range (-min and -max) and -ini file are required.',
            epilog = 'See https://github.com/kubikji2 for more silly projects.')

    # adding required arguments
    parser.add_argument('-min', '--min_temp', help="minimal temperature", required=True,
                            default=210, type=int)
    parser.add_argument('-max', '--max_temp', help="maximal temperature", required=True,
                            default=230, type=int)
    parser.add_argument('-ini', '--ini_profile', help="path to ini file, see README.md on how to create it", required=True)
    
    # adding optional arguments
    parser.add_argument('-step', '--step_temp', help="temperature step between consequentive floors", default=5)
    parser.add_argument('-fn', '--filename', help="final gcode filename", default=None)

    # try parsing arguments
    try:
        args = parser.parse_args()
    except SystemExit as err:
        # if failed on non-required argument, suggest using help
        if err.code == 2:
            print("'-> For more info see: {} -h.".format(__file__),file=sys.stderr)
        sys.exit(-1)
    
    # extract arguments
    _min_temp = args.min_temp
    _max_temp = args.max_temp
    _step_temp = args.step_temp
    _ini_path = args.ini_profile

    # extracting data from the ini file
    flh, lh, fil_name = extract_data_from_ini(_ini_path)
    fil_name = fil_name.replace(" ", "-").replace("\"", "")

    _final_fn = args.filename if args.filename is not None else "temperature_tower_{}-{}_{}.gcode".format(_min_temp, _max_temp, fil_name)
    
    produce_stl(_min_temp,_max_temp,_step_temp)
    produce_gcode()
    temperatures = [i for i in range(_min_temp,_max_temp+1,_step_temp)]
    processs_gcode(fn_out=_final_fn, temperatures=temperatures, first_layer_height=flh, layer_height=lh)
