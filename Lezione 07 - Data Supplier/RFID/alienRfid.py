import telnetlib

tn = telnetlib.Telnet("192.168.0.1", "8009")
tn.read_until(b"Username>")  # wait till prompted for username
tn.write(b"alien\r\n")
tn.read_until(b"Password>")  # wait till prompted for password
tn.write(b"password\r\n")
tn.read_until(b"Alien>")
print('here')
while True:
    tn.write(b"get TagList\r\n")  # enter commands
    response = tn.read_until(b'Alien>').decode("utf-8")
    print('....',response)

