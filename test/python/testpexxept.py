import pexpect

child = pexpect.spawn('ssh -fNg -R 7777:localhost:22 root@121.42.157.113')

# child.expect('The authen.*')
# print(child.before)
# child.sendline('yes')
# print('OK')
child.expect("root@121.42.157.113.*")
child.sendline('Apple2011')
# child.expect(pexpect.EOF)
# print(child.before)
# child.interact()
