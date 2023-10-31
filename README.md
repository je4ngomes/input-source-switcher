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
 "HOTKEY_TO_SWITCH": "ctrl+shift+["
}
```
If you are unsure of the monitor index, run `python input_source_switcher.py --list` to list all connected monitors and their index.\n
4. Create a shortcut from run.bat and move it to windows `C:\ProgramData\Microsoft\Windows\Start Menu\Programs`
  - Obs: If changes don't take effect immediately, try restarting the computer or just logging out and logging back in.

To change back to the previous input source from the other computer, you will need to run the script on that computer as well.

## Command line arguments
- `--list` - Lists all connected monitors and their index

## TODO
  - [ ] Add trigger to simultaneously switch the keyboard and mouse using [Synergy](https://github.com/amankhoza/synergy-binaries)
