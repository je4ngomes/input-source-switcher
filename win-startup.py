# Python code to add current script to the registry

# module to edit the windows registry 
import winreg as reg 
import os			 

def AddToRegistry():

	# in python __file__ is the instant of
	# file path where it was executed 
	# so if it was executed from desktop,
	# then __file__ will be 
 
	# c:\users\current_user\desktop
	# name of the python file with extension
	# joins the file name to end of path address
	address=os.path.join(os.path.dirname(os.path.realpath(__file__)),"input-source-switcher.py -f settings.json"	) 
	
	# open the key to make changes to
	open = reg.OpenKey(
	  # key we want to change is HKEY_CURRENT_USER 
    reg.HKEY_CURRENT_USER,
	  # key value is Software\Microsoft\Windows\CurrentVersion\Run
    "Software\Microsoft\Windows\CurrentVersion\Run",
    0,
    reg.KEY_ALL_ACCESS
  )
	
	# modify the opened key
	reg.SetValueEx(open,"any_name",0,reg.REG_SZ,address)
	
	# now close the opened key
	reg.CloseKey(open)

# Driver Code
if __name__=="__main__":
	AddToRegistry()
