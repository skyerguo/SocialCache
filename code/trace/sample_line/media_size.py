
import threading
import shlex
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class url_req(threading.Thread):
    def __init__(self, url_file):
        self.url_file = url_file
    
    def launch_request(self):
        pass

    def preprocess_data(self, filename):
        # get file lines number
        ret = subprocess.Popen()
        ret.wait()

    def run():
        pass

def main(filename):
    # prepare data
    thread_num = 7
    ret = subprocess.Popen(shlex.split("sh %s 7" %filename), stdout=subprocess.DEVNULL)
    ret.wait()

if __name__ == "__main__":
    print("run as main")
    # main("preprocess_data.sh")

    test_data = np.loadtxt("media_size.dat", dtype='int')
    test_data = test_data/1024
    print(test_data)
    print(type(test_data))
    print(test_data.shape)

    res_freq = stats.relfreq(test_data, numbins=1024)

    pdf_value = res_freq.frequency

    cdf_value = np.cumsum(res_freq.frequency)

    x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)

    plt.figure()
    plt.grid()
    plt.title("PDF of media size of twitter's user")
    plt.xlabel("media size(KB)")
    plt.ylabel("probability")
    plt.bar(x, pdf_value, width=res_freq.binsize)
    plt.savefig("pdf.png")
    
    plt.figure()
    plt.grid()
    plt.xlabel("media size(KB)")
    plt.ylabel("probability")
    plt.title("CDF of media size of twitter's user")
    plt.plot(x, cdf_value)
    plt.savefig("cdf.png")