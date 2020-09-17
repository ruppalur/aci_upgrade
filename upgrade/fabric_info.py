import json


#load the file locally for testing
#with open(f'/home/ruppalur/Dev/aup/sample_data/{fabricNode}.json') as fvnode:
#    fvnode_dict = json.load(fvnode)
#load the file locally for testing
#with open(f'/home/ruppalur/Dev/aup/sample_data/{firmwareRunning}.json') as nodefirmware:
#    nodefirmware = json.load(nodefirmware)

# based on the role assign the class

def fabric_node_fw(fabricNode_output,firmwareRunning_output):
	for object in fabricNode_output['imdata']:
		node = object['fabricNode']['attributes']['id']
		if len(node) > 2:
			for firmwareObject in firmwareRunning_output['imdata']:
				if (node in firmwareObject['firmwareRunning']['attributes']['dn']) and ('leaf' in object['fabricNode']['attributes']['role']):
					firmware = firmwareObject['firmwareRunning']['attributes']['version']
					object['fabricNode']['attributes']['firmware'] =  firmware
					object['fabricNode']['attributes']['element_class'] = 'info'
				elif (node in firmwareObject['firmwareRunning']['attributes']['dn']) and ('spine' in object['fabricNode']['attributes']['role']):
					firmware = firmwareObject['firmwareRunning']['attributes']['version']
					object['fabricNode']['attributes']['firmware'] =  firmware
					object['fabricNode']['attributes']['element_class'] = 'success'
		else:
			object['fabricNode']['attributes']['element_class'] = 'danger'

	return fabricNode_output