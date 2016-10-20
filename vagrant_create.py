from paramiko import SSHClient
import paramiko
import subprocess
import time
class jenkinsAutomation:
	def __init__(self,server,user,password):
		self.server = server
		self.user = user
		self.password = password

	def  command_run(command):
		process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
		for line in iter(process.stdout.readline, b''):
			print line,
		output = process.communicate()
		process.stdout.close()
		return output[0]

	def confing_vagrant(vmip):
		vagrant_file = open("Vagrantfile","w")
	
		ipconfig = '  config.vm.network "private_network", ip: "%s"\n'%vmip

		vagrant_file.write(ipconfig)

		vagrant_file.close()

	
	def ssh_server(self,cm1,cm2,src1,des1,src2,des2):

		client = SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.load_system_host_keys()
		client.connect(self.server, username=self.user, password=self.password)
		transport = paramiko.Transport((self.server,22))
		transport.connect(username=user, password=passwd)
		sftp = paramiko.SFTPClient.from_transport(t)
		sftp.put(src1,des1)
		sftp.put(src2,des2)

		stdin1, stdout1, stderr1 = client.exec_command(cm1)
		jenkins_ins = stdout1.readlines()

		stdin2, stdout2, stderr2 = client.exec_command(cm2)
        	jenkins_server = stdout2.readlines()
		for info in  jenkins_server:
			print info
if __name__ == "__main__":
	jenkins =  jenkinsAutomation('192.168.56.30','vagrant','root')
	jenkins.command_run("vagrant box add ")
	jenkins.command_run("vagrant init ")
	jenkins.config_vagrant("192.168.56.30")
	jenkins.command_run("vagrant up jenkins")
	jenkins.ssh_server("sudo sh /home/vagrant/jenkinstall.sh", "sudo service jenkins restart", "jenkins_config/jenkinstall.sh", "/home/vagrant/jenkinstall.sh", "jenkins_config/config.xml", "/home/vagrant/config.xml")


