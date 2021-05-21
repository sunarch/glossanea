# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from cli.output import CLIOutput


def main():

    argList = list(sys.argv)
    filename = argList.pop(0)
    arguments = argList
    argumentCount = len(arguments)

    try:
        if argumentCount == 0 or (argumentCount == 1 and arguments[0] == "--gui"):
            from gui.gui import GUI as ui

        elif argumentCount == 1 and arguments[0] == "--cli":
            from cli.cli import CLI as ui

        elif argumentCount == 1 and arguments[0] == "--help":
            invocation_help()
            sys.exit(0)
        
        elif argumentCount == 2 and arguments[0] == "--help" and arguments[1] == "--dev":
            invocation_help(display_dev=True)
            sys.exit(0)

        elif argumentCount in [1, 2] and arguments[0] == "--convert-data-v1-to-v2":
            arguments.pop(0)
            from utils.convert_data_v1_to_v2 import ConvertDataV1ToV2
            ConvertDataV1ToV2.run(arguments)
            sys.exit(0)

        else:
            raise ValueError("Illegal arguments")

    except ValueError as ve:
        CLIOutput.warning(ve)
        invocation_help()

    else:
        ui.start()

# help --------------------------------------------------------------- #

def invocation_help(display_dev=False):
    
    options = [
        ["--gui",   "[DEFAULT] Start with Graphical User Interface."],
        ["--cli",   "Start with Command Line Interface."],
        ["--help",  "Display this help text."]
    ]
    
    CLIOutput.empty_line(1)
    CLIOutput.simple("WOYO help")
    
    CLIOutput.empty_line(1)
    CLIOutput.value_pair_list(options, CLIOutput.FORMAT_REGULAR, CLIOutput.SPACING_CLOSE)
    
    if display_dev == True:

        dev_options = [
            ["--convert-data-v1-to-v2 all",        "Upgrade all data files."],
            ["--convert-data-v1-to-v2 DATA_FILE",  "Upgrade DATA_FILE."]
        ]
        
        CLIOutput.empty_line(1)
        CLIOutput.simple("WOYO developer options")
        
        CLIOutput.empty_line(1)
        CLIOutput.value_pair_list(dev_options, CLIOutput.FORMAT_REGULAR, CLIOutput.SPACING_CLOSE)

    

# script main start -------------------------------------------------- #

if __name__== "__main__":
    main()

# END ---------------------------------------------------------------- #
