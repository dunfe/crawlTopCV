import matplotlib.pyplot as plt
import numpy as np
from statistics import mean, stdev
from calculate import read_file


def draw_multiple_boxplot(majors):
    data = []
    for major in majors:
        _data = read_file(major)
        data.append(_data)
    draw_boxplot(data, majors)


def draw_boxplot(data, majors):
    fig, ax = plt.subplots()
    ax.boxplot(data)

    data_len = len(data)
    print(majors)
    plt.xticks(np.arange(data_len) + 1, majors, rotation=90)
    plt.yticks(np.arange(0, 110, step=10))
    ax.set_ylabel('Million VNĐ')
    ax.set_xlabel('Majors')

    plt.tight_layout()
    plt.savefig('boxplot.png')
    plt.show()


def draw_multiple_histogram(majors):
    for major in majors:
        data = read_file(major)
        draw_histogram(data, major)


def draw_histogram(data, name):
    mean_of_distribution = mean(data)
    standard_deviation = stdev(data)

    plt.xlabel = 'Value'
    plt.ylabel = 'Frequency'
    fig, ax = plt.subplots()

    num_bins = np.arange(0, max(data), 1)

    # the histogram of the data
    # n: The values of the histogram bins
    n, bins, patches = ax.hist(data, bins=num_bins, density=True)

    # Vẽ đường best fit
    y = ((1 / (np.sqrt(2 * np.pi) * standard_deviation)) *
         np.exp(-0.5 * (1 / standard_deviation * (bins - mean_of_distribution)) ** 2))

    ax.plot(bins, y, '--')
    ax.set_xlabel('Million VNĐ')
    ax.set_ylabel('Probability density')
    ax.set_title(r'Histogram of ' + name)

    print('n', n, sum(n))
    print('bins: ', bins)
    print('patches: ', patches)

    # Vẽ đường trung vị
    print('Mean: ', mean_of_distribution)
    plt.axvline(mean_of_distribution, color="red", label="Mean of distribution")

    fig.tight_layout()
    save_path = 'C:/Users/dung2/PycharmProjects/crawlTopCV/image/' + name + '.png'
    # plt.savefig(save_path)
    plt.show()

