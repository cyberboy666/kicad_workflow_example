# kicad_workflow_example
an example kicad project to experiment with automated workflows

## goals

on every git _push_:
- check the schematic and pcb tester for problems (dont block just alert if there is something)

on every git _release_:
- run checkers...
- export schematic pdf
- export gerber files (lastest.zip format ?)
- export the bom's (full, tayda, mouser ibom)
