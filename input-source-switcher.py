import argparse
import json
import asyncio
import logging
import keyboard

from logging.handlers import RotatingFileHandler
from monitorcontrol import get_monitors, InputSource

# Create a rotating file handler that logs to 'input-source-switcher.log', with a maximum size of 1MB and a backup count of 1
logginHandler = RotatingFileHandler('input-source-switcher.log', maxBytes=1000000, backupCount=1)

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
monitors = get_monitors()

def read_config_file(file_path):
  with open(file_path, 'r') as f:
    return json.load(f);
  
# function that return a dictory of monitor name and inputs, if monitor with same name is found add count property
def get_monitor_inputs():
  monitors_dict = {}
  
  for monitor in monitors:
    with monitor:
      caps = monitor.get_vcp_capabilities()
      
      model = caps['model']
      if model in monitors_dict:
        monitors_dict[model]['count'] += 1
      else:
        monitors_dict[model] = {
          'inputs': caps['inputs'],
          'monitor': monitor,
          'count': 1,
        }
      
  return monitors_dict
  
def list_monitors():
  monitors_inputs = get_monitor_inputs()
  
  for monitor, value in monitors_inputs.items():
    print('Monitor Model: {}'.format(monitor))
    print('Input sources: {}'.format(
      ', '.join(
        input_source.name for input_source in value['inputs']
        )
      )
    )
    print('Count: {}'.format(value['count']))
    print('=' * 30)
  
def setup_args():
  parser = argparse.ArgumentParser(description='Monitor Control')
  
  parser.add_argument(
    '--list',
    help='list monitors',
    action='store_true',
  )
  
  parser.add_argument(
    '-f',
    metavar='file',
    type=str,
    help='The path to the JSON file to read',
    dest='file',
    required=False,
  )
  
  args = parser.parse_args();
  
  if args.list:
    return list_monitors()
    
  if args.file is None:
    msg = 'Settings file required. Use -f or --file to specify a file'
    logging.error(msg)
    raise Exception(msg)

  if not args.file.endswith('.json'):
    msg = 'File must be a JSON file'
    logging.error(msg)
    raise Exception(msg)

  return args

def toggle_monitor_input(config, monitors_inputs):  
  model = config['model']
  input_source_1 = config['input_source_1']
  input_source_2 = config['input_source_2']

  if monitors_inputs.get(model):
    monitor = monitors_inputs[model]['monitor']
    with monitor:
      current_input = monitor.get_input_source()
      
      if current_input == input_sources[input_source_1]:
        logging.info('Switching monitor input to {}'.format(input_source_2))
        # monitor.set_input_source(input_sources[input_source_2])
      elif current_input == input_sources[input_source_2]:
        logging.info('Switching monitor input to {}'.format(input_source_1))
        # monitor.set_input_source(input_sources[input_source_1])
      else:
        logging.error('Monitor {} is not set to either input source'.format(model))
  else:
    logging.error('Monitor {} is not connected'.format(model))


args = setup_args()

#load file settings
file_settings = read_config_file(args.file)

async def main():
  execution_start_time = asyncio.get_running_loop().time()
  monitors_inputs = get_monitor_inputs()
  
  
  tasks = [
    asyncio.to_thread(
      toggle_monitor_input, monitor, monitors_inputs
    ) for monitor in file_settings['monitors']
  ]
  
  await asyncio.gather(*tasks)  
  execution_end_time = asyncio.get_running_loop().time()
  
  logging.info('Took {} seconds'.format(execution_end_time - execution_start_time))
  logging.shutdown()
  
  
def on_hotkey_press(*args):
  logging.info('Hotkey pressed, initiating monitor input switch')
  asyncio.run(main())
  


try:
  logging.info('Program started...')
  keyboard.add_hotkey(file_settings['HOTKEY_TO_SWITCH'], on_hotkey_press)
  
  print('Press ESC to stop') 
  keyboard.wait('esc')
except KeyboardInterrupt:
  print('Exiting...')
  logging.info('Exiting...')
  logging.shutdown()