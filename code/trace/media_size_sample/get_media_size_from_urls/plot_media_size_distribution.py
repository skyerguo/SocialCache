import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

if __name__ == "__main__":
    print("======= run as main =======")
    # main("preprocess_data.sh")

    test_data = np.loadtxt("media_size.dat", dtype='int')
    test_data = test_data/1024

    res_freq = stats.relfreq(test_data, numbins=1024)

    pdf_value = res_freq.frequency
    cdf_value = np.cumsum(res_freq.frequency)

    x = res_freq.lowerlimit + np.linspace(0, res_freq.binsize * res_freq.frequency.size, res_freq.frequency.size)

    res_dir = "./table/"
    if not os.path.exists(res_dir):
        os.mkdir(res_dir)

    plt.figure()
    plt.grid()
    plt.title("PDF of media size of twitter's user")
    plt.xlabel("media size(KB)")
    plt.ylabel("probability")
    plt.bar(x, pdf_value, width=res_freq.binsize)
    plt.savefig(res_dir + "media_size_pdf.png")
    
    plt.figure()
    plt.grid()
    plt.xlabel("media size(KB)")
    plt.ylabel("probability")
    plt.title("CDF of media size of twitter's user")
    plt.plot(x, cdf_value)
    plt.savefig(res_dir + "media_size_cdf.png")