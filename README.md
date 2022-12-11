# Temperature Tower Generator

Utility for creating customizable temperature towers for filament temperature calibration. [OpenSCAD](https://openscad.org/) is used for creating a model, [PrusaSlicer](https://www.prusa3d.com/page/prusaslicer_424/) is used to create gcode and [Python](https://www.python.org/) is used to coordinate the effort.

## Roadmap

### Openscad - Core model

This step will be implemented in `source/floor.scad` file.

- [x] model basic slopes at two different angles with holes
- [x] add bridging segment
- [x] add stringing segment (two cones)
- [ ] add curvature segment 

### Openscad - Tower model

This step will be implemented in `source/tower.scad` file.

- [ ] replicate floors to form a tower
- [ ] add baseplate using [Q++ OpenSCAD library](https://github.com/kubikji2/qpp-openscad-library)
- [ ] add text for temperatures and material
- [ ] make it easily interfacable as in [url-qr-stl](https://github.com/kubikji2/url-qr-stl)
