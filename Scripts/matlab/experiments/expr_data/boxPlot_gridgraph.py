import numpy as np
import matplotlib.pyplot as plt

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)



def main():
    myfile = open('experiment.txt', 'r')
    data = {}
    # p and graphname are the same in whole dataset
    for line in myfile:
        graphname, p, install, steps, tau = line.split()
        install = float(install)
        steps = int(steps)
        tau = float(tau)
        if install in data:
            if steps in data[install]:
                data[install][steps].append(tau)
        
            else:
                data[install][steps] = [tau]
        else:
            data[install] = {steps:[tau]}

    box_data = [data[0.1][steps] for steps in sorted(data[0.1])]
    box_data2 = [data[0.2][steps] for steps in sorted(data[0.2])]
    ticks = sorted(data[0.1].keys())
    plt.figure()
    bpl = plt.boxplot(box_data, positions=np.array(xrange(len(box_data)))*2.0-0.4, sym='', widths=0.7)
    bpr = plt.boxplot(box_data2, positions=np.array(xrange(len(box_data2)))*2.0+0.4, sym='', widths=0.7)
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
    plt.savefig('Gridsoc_katx_vskatz_kendall.png')
    #plt.show()
    
    
if __name__ == '__main__':
    main()
