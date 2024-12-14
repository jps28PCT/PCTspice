# PCTspice
PCTspice is a DC circuit solver written in Python. 
Using a command-line interface, users can input circuit branches containing start node, componenet, and end node, and can return nodal and component voltages and component currents.
PCTspice is designed to be similar to traditional SPICE CLI programs while improving readibility and ease of use.

## Running PCTspice
A Python interpreter must be installed to run.  The SymPy module is also neccesary to use the PCTspice program.  
To install, open command prompt and type 'pip install sympy'.  This uses Python's native package installer.

> [!NOTE]
> PCTspice requires Python 3.11 or later to function.
> SymPy 1.13.3 or later is also required to run.

PCTspice opens directly into its CLI, and commands can be run at any time.  Type `HELP` for more information!

This program makes heavy use of ANSI escape codes, which most modern terminal emulators and command lines support.
These control features like text color and clearing the terminal.  If the text color is white exclusively and the ANSI escape codes are being printed to the screen as text, then commands like 'CLEAR' will not work.


## Inputs and Commands
At any point during execution of PCTspice, a command or branch description may be entered.

### Branch Description and Component Entry
Format:     
  `[Start node name] [Component name]=[Component value] [End node name]`

  or        
    `[Start node name] [Component name] [End node name]`
    `[Component name]=[Component value]`
       
-  Input is not case-sensitive, except for any engineering notation prefix entered.
-  The start node is considered the positive terminal of a the component.  Any alphanumeric string less than 5 characters is accepted.  Use 'GND' for reference ground.
-  The component name must be the type of component and a unique number; Like 'R1' or 'V2'.  Any length of number can be used, and they do not have to be sequential.
   Types of components:
      - '`V`' for ideal DC voltage source.
      - '`I`' for ideal DC current source.
      - '`R`' for non-reactive resistor.
   
   Units are implied by the type of component selected.
      - 'Volts' for voltage source.
      - 'Amperes' for current source.
      - 'Ohms' for resistor.
     
-   Component values should be entered in without any unit.
    Engineering notation prefixes can be used immediately after the number with no space.
    Valid prefixes:
    | Symbol | Prefix | Power | | Symbol | Prefix | Power |
    | :---: | :--- | :---: | --- | :---: | :--- | :---: |
    | '`T`' | tera- | 10<sup>12</sup> | | '`p`' | pico- | 10<sup>-12</sup> |
    | '`G`' | giga- | 10<sup>9</sup> | | '`n`' | nano- | 10<sup>-9</sup> |
    | '`M`' | mega- | 10<sup>6</sup> | | '`u`' | micro- | 10<sup>-6</sup> |
    | '`K`' | kilo- | 10<sup>6</sup>  | | '`m`' | milli- | 10<sup>-3</sup> |
    
    Examples: `R1=10K`   creates a resistor R1 with a value of 10 kilo-ohms.
              `I2=530u`  creates a current source I2 with a value of 530 microamps.
  
-   The end node is considered the negative terminal of the component.  Any alphanumeric string less than 5 characters is accepted.  Use 'GND' for reference ground.
