import paramiko
import interactive

sshClient = paramiko.client.SSHClient()
sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sshClient.connect('localhost', username='stargazer', password='Apple2011')

chan = sshClient.invoke_shell()
interactive.interactive_shell(chan)
chan.close()
sshClient.close()
