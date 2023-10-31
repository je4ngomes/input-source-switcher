# input-source-switcher
Python script designed to enable seamless switching between two different monitor input sources through the use of a customizable hotkey.

## Requirements
- [Python 3](https://www.python.org/downloads/)

## Usage
1. Clone the repository
2. Install the required packages using `pip install -r requirements.txt`
3. Setup settings in `settings.json`, e.g.:
```json
{
  "monitors": [
    {
      "model": "VP249QGR",
      "input_source_1": "DP1",
      "input_source_2": "HDMI1",
      "monitor_index": 1
    },
    {
      "model": "24G2HE5",
      "input_source_1": "HDMI1",
      "input_source_2": "ANALOG1",
      "monitor_index": 2
    },
    {
      "model": "24G2HE5",
      "input_source_1": "HDMI2",
      "input_source_2": "ANALOG1",
      "monitor_index": 3
    }
 ],
  "TRIGGER_SYNERGY": false
}
```
If you are unsure of the monitor index, run `python input_source_switcher.py --list` to list all connected monitors and their index.\n
3. Edit `run.bat` to point to the correct python executable and script path
4. Create a shortcut from run.bat and move it to windows `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`
5. Add a hotkey to the shortcut by right clicking on the shortcut, selecting properties and then setting the shortcut key
  <p align="center">
    <img src="https://github.com/je4ngomes/input-source-switcher/blob/main/img/hotkey.jpg?raw=true" alt="Sublime's custom image"/>
  </p>
  - Obs: If changes don't take effect immediately, try restarting the computer or just logging out and logging back in.

To change back to the previous input source from the other computer, you will need to run the script on that computer as well.

## Synergy integration
To enable seamless switching between the two computers, you can use [Synergy](https://github.com/DEAKSoftware/Synergy-Binaries) to share the keyboard and mouse between the two computers. To do so, follow the steps below:
1. Install Synergy on both computers
2. Configure Synergy to share the keyboard and mouse between the two computers
3. Configure two hotkeys on Synergy:
    - To switch between the two computers
    - To toggle locking the mouse to the current computer
4. Edit `settings.json` to specify `True` or `False` on `TRIGGER_SYNERGY`

## Command line arguments
- `--list` - Lists all connected monitors and their index

## TODO
  - [x] Add trigger to simultaneously switch the keyboard and mouse using **Synergy**
