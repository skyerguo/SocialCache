import subprocess

sub = int(subprocess.getoutput("python3 -m code.analyze.get_media_size -n 0"))
print(sub)
# sub.wait()
# res = sub.stdout.read()
# print("******* simulator done, get res ", res)