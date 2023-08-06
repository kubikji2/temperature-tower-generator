import os, sys

import argparse

STL_FILENAME = "temp-tower-test.stl"
GCODE_FILENAME = "temp-tower-test.gcode"

# extract value from the lines
def get_value_at_line(l):
    return l[0].strip().split(" = ")[-1]


# extract data from the provided ini file
def extract_data_from_ini(fn_config):

    with open(fn_config, 'r') as f:
        bundle_lines = f.readlines()
        layer_height = float(get_value_at_line([line for line in bundle_lines if line.startswith("layer_height")]))
        first_layer_height = float(get_value_at_line([line for line in bundle_lines if line.startswith("first_layer_height")]))
        filament_name = get_value_at_line([line for line in bundle_lines if line.startswith("filament_settings_id")])
        printer_name = get_value_at_line([line for line in bundle_lines if line.startswith("printer_model")])
    
    return first_layer_height, layer_height, filament_name, printer_name


# create stl using OpenSCAD
def produce_stl(min_temp, max_temp, step_temp, filament_name, printer_name, stl_fn=STL_FILENAME):
    
    print("[DEBUG] producing stl. It might take a few minutes.")
    
    cmd_template = "openscad -o {} source/tower.scad -D min_temp={} -D max_temp={} -D step_temp={} -D material={} -D printer={}"
    cmd = cmd_template.format(stl_fn, min_temp, max_temp, step_temp, filament_name, printer_name)
    os.system(cmd)

    print("[DEBUG] stl finished.")


# slice stl using PrusaSlicer
def produce_gcode(fn_config, fn_in=STL_FILENAME, fn_out=GCODE_FILENAME):

    print("[DEBUG] slicing.")

    cmd_template = "prusaslicer -g {} --load {} -o {}"
    cmd = cmd_template.format(fn_in, fn_config, fn_out)
    os.system(cmd)

    print("[DEBUG] slicing finished.")

# process gcode, aka add temperature changes
def processs_gcode(first_layer_height, layer_height, temperatures, fn_final, fn_in=GCODE_FILENAME):
    
    print("[DEBUG] starting gcode modification.")

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
    with open(fn_final,'w') as f:
        f.write(gcode_lines)

    print("[DEBUG] final gcode done.")

#DEFFAULT_MIN_TEMP = 210
#DEFFAULT_MAX_TEMP = 230
DEFFAULT_TEMP_STEP = 5

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            prog = '{}'.format(__file__),
            description = 'Creates gcode for temperature tower to select an optimal printing temperature. The temperature range (-min and -max) and -ini file are required.',
            epilog = 'See https://github.com/kubikji2 for more silly projects.')

    # adding required arguments
    parser.add_argument('-min', '--min_temp', help="minimal temperature", required=True, type=int)
    parser.add_argument('-max', '--max_temp', help="maximal temperature", required=True, type=int)
    parser.add_argument('-ini', '--ini_profile', help="path to ini file, see README.md on how to create it", required=True)
    
    # adding optional arguments
    parser.add_argument('-step', '--step_temp', help="temperature step between consequentive floors  ({} default)".format(DEFFAULT_TEMP_STEP),
                            default=DEFFAULT_TEMP_STEP, type=int)
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
    flh, lh, file_name, printer_name = extract_data_from_ini(_ini_path)
    file_name = file_name.replace(" ", "-").replace("\"", "").replace("(","_").replace(")","_")

    _final_fn = args.filename if args.filename is not None else "temperature_tower_{}-{}_{}.gcode".format(_min_temp, _max_temp, file_name)
    
    # filament type and printer name including the quotation marks
    _filament_name = "\\\"{}\\\"".format(file_name)
    _printer_name = "\\\"{}\\\"".format(printer_name)

    print("[DEBUG] argument processing done.")

    # create stl
    produce_stl(_min_temp,_max_temp,_step_temp,_filament_name,_printer_name)
    
    # create gcode
    produce_gcode(fn_config=_ini_path)
    
    # process gcode
    temperatures = [i for i in range(_min_temp,_max_temp+1,_step_temp)]
    processs_gcode(temperatures=temperatures, first_layer_height=flh, layer_height=lh, fn_final=_final_fn)

