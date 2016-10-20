
import subprocess
def  command_run(command):
	process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	for line in iter(process.stdout.readline, b''):
		print line,
	output = process.communicate()
	process.stdout.close()
	return output[0]

def vagrant_config(vmip):
	vagrant_file = open("Vagrantfile","w")
	
	ipconfig = '  config.vm.network "private_network", ip: "%s"\n'%vmip

	vagrant_file.write(ipconfig)

	vagrant_file.close()

	return "Vagrantfile written"
if __name__ == "__main__":
	print command_run("vagrant box add ")
	print command_run("vagrant init ")
	print vagrant_config("")
	print command_run("vagrant up jenkins")
