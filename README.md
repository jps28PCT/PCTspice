# PCTspice
PCTspice is a DC circuit solver written in Python. <BR />

Using a command-line interface, users can input circuit branches containing start node, componenet, and end node, and can return nodal and component voltages and component currents.<BR />

PCTspice is designed to be similar to traditional SPICE CLI programs while improving readibility and ease of use.

## Running PCTspice
A Python interpreter must be installed to run.  The SymPy module is also neccesary to use the PCTspice program. <BR /> 
To install, open command prompt and type 'pip install sympy'.  This uses Python's native package installer.

> [!NOTE]
> PCTspice requires Python 3.11 or later to function.<BR />
> SymPy 1.13.3 or later is also required to run.

PCTspice opens directly into its CLI, and commands can be run at any time.  Type `HELP` for more information!

This program makes heavy use of ANSI escape codes, which most modern terminal emulators and command lines support.<BR />
These control features like text color and clearing the terminal.  If the text color is white exclusively and the ANSI escape codes are being printed to the screen as text, then commands like 'CLEAR' will not work.


## Inputs and Commands
At any point during execution of PCTspice, a command or branch description may be entered.

<details>
<summary>Branch Description and Component Entry</summary>
       
Format:     
    `[Start node] [Component]=[Value] [End node]`<BR />
 or        
    `[Start node] [Component] [End node]`<BR />
    `[Component]=[Value]`
       
-  Input is not case-sensitive, except for any engineering notation prefix entered.
-  The start node is considered the positive terminal of a the component.  Any alphanumeric string less than 5 characters is accepted.  Use '`GND`' for reference ground.
-  The component name must be the type of component and a unique number; Like 'R1' or 'V2'.  Any length of number can be used, and they do not have to be sequential.<BR />

   Types of components:
      - '`V`' for ideal DC voltage source.
      - '`I`' for ideal DC current source.
      - '`R`' for non-reactive resistor.
   
   Units are implied by the type of component selected.
      - 'Volts' for voltage source.
      - 'Amperes' for current source.
      - 'Ohms' for resistor.
     
-   Component values should be entered in without any unit.
    Engineering notation prefixes can be used immediately after the number with no space.<BR />
    
    Valid prefixes:
    | Symbol | Prefix | Power | | Symbol | Prefix | Power |
    | :---: | :--- | :---: | --- | :---: | :--- | :---: |
    | '`T`' | tera- | 10<sup>12</sup> | | '`p`' | pico- | 10<sup>-12</sup> |
    | '`G`' | giga- | 10<sup>9</sup> | | '`n`' | nano- | 10<sup>-9</sup> |
    | '`M`'<br />'`MEG`' | mega- | 10<sup>6</sup> | | '`u`' | micro- | 10<sup>-6</sup> |
    | '`K`' | kilo- | 10<sup>3</sup>  | | '`m`' | milli- | 10<sup>-3</sup> |
    
    Examples:<BR />
      `R1=10K`   creates a resistor R1 with a value of 10 kilo-ohms. <BR />
      `I2=530u`  creates a current source I2 with a value of 530 microamps.
  
-   The end node is considered the negative terminal of the component.  Any alphanumeric string less than 5 characters is accepted.  Use '`GND`' for reference ground.
</details>

<details>
<summary>List of commands</summary>
       
| Command | Description |
| :--- | :--- |
| `CLEAR` | Clears terminal window. |
| `EDIT [component]=[new value]` | Change component value to new value. |
| `EDIT BRANCH [#]`<br />`> [Start node] [Component]=[Value] [End node]` | Edit branch information, including start node, end node, and componenet name.<br />The number is found using the `PRINT BRANCHES` command. |
| `END` | End session of PCTspice. |
| `HELP` | Prints out help message that contains information on inputs and commands. |
| `IMPORT [file name and path].txt` | Import text file that contains branch descriptions. |
| `NEW` | Clears memory and allows for new branch descriptions to be run. |
| `PRINT BRANCHES` | Prints current branch descriptions entered in memory. |
| `PRINT Components` | Prints current components and component values entered in memory. |


       
</details>
