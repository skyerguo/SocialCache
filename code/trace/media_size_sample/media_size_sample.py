import shlex
import os
import subprocess

class media_size_sample:
    def __init__(self):
        self.path = path = os.path.split(os.path.realpath(__file__))[0]
        self.population = self.path + '/' + "population"

    def sample(self, num):
        shell_cmd = "shuf %s -n %d" %(self.population, num)
        ret = subprocess.Popen(shlex.split(shell_cmd), stdout=subprocess.PIPE)
        result = ret.communicate()[0].decode('utf-8')
        ret.wait()

        res_list = result.split()
        return list(map(int, res_list))

if __name__ == "__main__":
    sp = media_size_sample()
    res = sp.sample(10)
    print(res)
