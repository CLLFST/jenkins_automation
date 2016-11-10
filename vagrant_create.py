import os
from paramiko import SSHClient
import paramiko
import subprocess
import time
class jenkinsAutomation:
	def __init__(self,server,user,password):
		self.server = server
		self.user = user
		self.password = password

	def  command_run(self,command):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
		for line in iter(process.stdout.readline, b''):
			print line,
		output = process.communicate()
		process.stdout.close()
		return output[0]

	def config_vagrant(self,vmip):
		f = open("Vagrantfile", "r")
		contents = f.readlines()
		f.close()
		vag_box = '  config.vm.box = "deb/wheezy-amd64"'

		ipconfig = '  config.vm.network "private_network", ip: "%s"\n'%vmip
		contents.insert(15, vag_box)
		contents.insert(17, ipconfig)
			
		vagrant_file = open("Vagrantfile", "w")
	
		contents = "".join(contents)
		for line in contents:
			if line!='  config.vm.box = "base"'+"\n":
				vagrant_file.write(line)

		vagrant_file.close()

	
	def ssh_server(self,cm1,cm2,src,des):

		client = SSHClient()

		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		client.load_system_host_keys()

		client.connect(self.server, username=self.user, password=self.password)
		transport = paramiko.Transport((self.server,22))

		transport.connect(username=self.user, password=self.password)

		sftp = paramiko.SFTPClient.from_transport(transport)

		parent = os.path.expanduser(src)

		for dirpath, dirnames, filenames in os.walk(parent):
    			remote_path = os.path.join(des, dirpath[len(parent)+1:])
        		try:
            			sftp.listdir(remote_path)
        		except IOError:
            			sftp.mkdir(remote_path)

        		for filename in filenames:
            			sftp.put(os.path.join(dirpath, filename), os.path.join(remote_path, filename))		
			
		
		stdin1, stdout1, stderr1 = client.exec_command(cm1)

		jenkins_ins = stdout1.readlines()

		stdin2, stdout2, stderr2 = client.exec_command(cm2)

        	jenkins_server = stdout2.readlines()

		for info in  jenkins_server:
			print info
if __name__ == "__main__":
	jenkins =  jenkinsAutomation("192.168.56.30","vagrant","vagrant")
	
	jenkins.command_run("vagrant init ")
	jenkins.config_vagrant("192.168.56.30")
	jenkins.command_run("vagrant up ")
	jenkins.ssh_server("sudo sh /home/vagrant/install_jenkins.sh", "sudo service jenkins restart", "jenkins_config/", "/home/vagrant")


