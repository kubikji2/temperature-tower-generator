# Temperature Tower Generator

Utility for creating customizable temperature towers for filament temperature calibration. [OpenSCAD](https://openscad.org/) is used for creating a model, [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) is used to create gcode and [Python](https://www.python.org/) is used to coordinate the effort.

## Pipeline (I want to know, how it works)

1. Running `temperature-tower.py` script with available arguments:
   - `--min-temp`/`-min` minimal temperature
   - `--max-temp`/`-max` maximum temperature
   - `--bed-temp`/`-bed` bed temperature
   - `--step-temp`/`-step` temperature increment step, default 5 °C
   - PLANNED: use a `--filament-name`/`-fln` to extract the PrusaSlicer filament present
2. Python script then:
   - runs OpenSCAD to produce `*.stl` using the available arguments
   - extract the level height from the script interface using tagged echo output
   - run PruslaSlicer to produce `*.gcode` using the local directory with settings
     - PLANNED: update the filament settings database from PrusaSlicer
   - process `*.gcode` by setting the temperature change in each temperature tower level
     - based on [this link](https://www.thingiverse.com/thing:2729076)
     - the `M104 S<temp>` is added after `;<leayer-height>` followed by two empty lines
   - save new gcode

## Roadmap

### Openscad - Core model

This step will be implemented in `source/floor.scad` file.

- [x] model basic slopes at two different angles with holes
- [x] add bridging segment
- [x] add stringing segment (two cones)
- [ ] add curvature segment 

### Openscad - Tower model

This step will be implemented in `source/tower.scad` file.

- [x] replicate floors to form a tower
- [x] add baseplate using [Q++ OpenSCAD library](https://github.com/kubikji2/qpp-openscad-library)
- [x] add text for temperatures ~~and material~~
- [x] make it easily interfacable as in [url-qr-stl](https://github.com/kubikji2/url-qr-stl)
