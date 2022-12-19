import os, sys, subprocess

def produce_stl(min_temp, max_temp, step_temp, fn="temp-tower-test.stl"):
    tmp_fn = "_tmp_tn.txt"
    cmd_template = "openscad -o {} source/tower.scad -D min_temp={} -D max_temp={} -D step_temp={}"
    cmd = cmd_template.format(fn, min_temp, max_temp, step_temp, tmp_fn)
    #os.system(cmd)

    proc = subprocess.run([cmd.split(" ")[0], *cmd.split(" ")[1:]], check=True)
    
    #(out, err) = proc.communicate()
    #print(out)
    #print(err)

    #out = subprocess.check_output(cmd, stdout=subprocess.PIPE, shell=True)
    out = proc.output
    lines = out.decode("utf-8")
    print(lines)
    lines = lines.split("/n")
    print(lines)
    #bph = [line for line in lines if "bph" in line][0].replace("\"","").split()
    #print(bph)
    #[0].split()[-1]
    #print(bph)

    #os.system(cmd)

if __name__=="__main__":
    produce_stl(200,210,5)
    # TODO ARG-parse
