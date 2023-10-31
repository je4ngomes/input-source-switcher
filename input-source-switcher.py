import argparse
import json
import asyncio
import logging
import os
import pyautogui

from logging.handlers import RotatingFileHandler
from monitorcontrol import get_monitors, InputSource

# Create a rotating file handler that logs to 'input-source-switcher.log', with a maximum size of 1MB and a backup count of 1
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input-source-switcher.log')
logginHandler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=1)

# Set the log format to include the time
formatter = logging.Formatter('%(asctime)s %(message)s')
logginHandler.setFormatter(formatter);
logging.basicConfig(level=logging.INFO, handlers=[logginHandler])

input_sources = {
  'HDMI1': InputSource.HDMI1,
  'HDMI2': InputSource.HDMI2,
  'ANALOG1': InputSource.ANALOG1,
  'ANALOG2': InputSource.ANALOG2,
  'DP1': InputSource.DP1,
  'DP2': InputSource.DP2,
}

def read_config_file():
  file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.json")
  with open(file_path, 'r') as f:
    return json.load(f);
  
# function that return a dictory of monitor name and inputs, if monitor with same name is found add count property
def get_detected_monitors() -> list[dict]:
  detected_monitors = []

  for index, monitor in enumerate(get_monitors(), 0):
    with monitor:
      caps = monitor.get_vcp_capabilities()

      detected_monitors.append({
        'monitor_ctx': monitor,
        'model': caps['model'],
        'inputs': caps['inputs'],
        'index': index+1,
      })
      
  return detected_monitors
  
def list_monitors():
  detected_monitors = get_detected_monitors()
  
  # for monitor, value in monitors_inputs.items():
  for detected_monitor in detected_monitors:
    print('Monitor Model: {}'.format(detected_monitor.get('model')))
    print('Input sources: {}'.format(
      ', '.join(
        input_source.name for input_source in detected_monitor.get('inputs')
        )
      )
    )
    print('Monitor index: {}'.format(detected_monitor.get('index')))
    print('=' * 30)
  
def setup_args():
  parser = argparse.ArgumentParser(description='Monitor Control')
  
  parser.add_argument(
    '--list',
    help='list monitor details to fill in settings.json',
    action='store_true',
  )
  
  args = parser.parse_args();
  
  if args.list:
    list_monitors();
    exit();

  return args

def toggle_monitor_input(config, detected_monitors):  
  model = config['model']
  monitor_index = config['monitor_index']
  input_source_1 = config['input_source_1']
  input_source_2 = config['input_source_2']

  for detected_monitor in detected_monitors:
    if detected_monitor.get('index') == monitor_index and detected_monitor.get('model') == model:
      monitor = detected_monitor['monitor_ctx']
      with monitor:
        current_input = monitor.get_input_source()
    
        if current_input == input_sources[input_source_1]:
          logging.info('Switching monitor input to {}'.format(input_source_2))
          monitor.set_input_source(input_sources[input_source_2])
        elif current_input == input_sources[input_source_2]:
          logging.info('Switching monitor input to {}'.format(input_source_1))
          monitor.set_input_source(input_sources[input_source_1])
        else:
          logging.error('Monitor {} is not set to either input source'.format(model))


args = setup_args()

#load file settings
file_settings = read_config_file()

async def main():
  execution_start_time = asyncio.get_running_loop().time()
  detected_monitors = get_detected_monitors()
  
  
  tasks = [
    asyncio.to_thread(
      toggle_monitor_input, monitor_settings, detected_monitors
    ) for monitor_settings in file_settings['monitors']
  ]
  
  await asyncio.gather(*tasks)  
  
  if (file_settings.get('TRIGGER_SYNERGY', False)):
    logging.info('Triggering synergy')
    logging.info('Switching mouse and keyboard')
    pyautogui.hotkey('ctrl', 'shift', '<');
    logging.info('Locking mouse to screen');
    pyautogui.hotkey('ctrl', 'shift', '>'); 
  
  execution_end_time = asyncio.get_running_loop().time()
  
  logging.info('Took {} seconds'.format(execution_end_time - execution_start_time))
  logging.shutdown()
  

if __name__ == '__main__':
  try:
    logging.info('Script triggered')
    asyncio.run(main())
  except:
    logging.info('Exiting...')
    logging.shutdown()
    exit()
  
