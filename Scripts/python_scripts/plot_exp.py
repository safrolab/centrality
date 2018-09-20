import matplotlib.pyplot as plt
import numpy as np


def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)


if __name__ == '__main__':
    data = np.genfromtxt('myexperiment.txt')
    exp = {}
    for i, j in data:
        i = int(i)
        if i in exp:
            exp[i].append(j)
        else:
            exp[i] = [j]
    bx_data = [exp[i] for i in sorted(exp)]
    data2 = np.genfromtxt('myexperiment20.txt')
    exp2 = {}
    for i, j in data2:
        i = int(i)
        if i in exp2:
            exp2[i].append(j)
        else:
            exp2[i] = [j]
    bx_data2 = [exp2[i] for i in sorted(exp2)]
    #plt.figure()
    #plt.xticks(fontsize=16)
    #plt.yticks(fontsize=16)
    #plt.boxplot(bx_data,
    #            showfliers=True, labels=sorted(exp.keys()))
    
    #plt.savefig('soc_bc_vsbc_kendall.png')
    #plt.show()

    ticks = sorted(exp.keys())

    plt.figure()

    bpl = plt.boxplot(bx_data, positions=np.array(xrange(len(bx_data)))*2.0-0.4, sym='', widths=0.7)
    bpr = plt.boxplot(bx_data2, positions=np.array(xrange(len(bx_data2)))*2.0+0.4, sym='', widths=0.7)
    set_box_color(bpr, '#D7191C') # colors are from http://colorbrewer2.org/
    set_box_color(bpl, '#2C7BB6')

    # draw temporary red and blue lines and use them to create a legend
    plt.plot([], c='#D7191C', linewidth=4, label=r'$|\Omega|/|V| = 0.2$')
    plt.plot([], c='#2C7BB6', linewidth=4,label=r'$|\Omega|/|V| = 0.1$')
    plt.legend()

    plt.xticks(xrange(0, len(ticks) * 2, 2), ticks)
    plt.xlim(-2, len(ticks)*2)
    plt.ylim(0, 1.3)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig('soc_bc_vsbc_kendall.png')
    plt.show()
