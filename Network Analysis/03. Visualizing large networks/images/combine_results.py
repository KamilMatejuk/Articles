import re
import glob
import matplotlib.pyplot as plt


def generate(prefix: str, orders: list[int] = None):
    files = sorted(list(glob.glob(f'../results/{prefix}_*.png')))
    if orders is not None:
        files = [files[i] for i in orders]

    fig, axes = plt.subplots(1, len(files), figsize=(12, 12 / len(files) + 0.5))

    for i, filename in enumerate(files):
        label = re.search(rf'{prefix}_(.+).png', filename).group(1).title()
        axes[i].imshow(plt.imread(filename))    
        axes[i].set_title(label)
    
    for ax in axes: ax.axis('off')
    fig.tight_layout()
    plt.savefig(f'combined_results_{prefix}.png')


if __name__ == '__main__':
    # generate('basic', orders=[2, 1, 0, 3])
    # generate('nx', orders=[1, 0, 2, 3, 4])
    # generate('edge_visibility_based_on_degree_lin', orders=[1, 0, 2, 3])
    # generate('edge_visibility_based_on_degree_pow', orders=[1, 0, 2, 3])
    # generate('node_visibility_based_on_degree', orders=[1, 0, 2, 3])
    # generate('node_sorted_by_degree', orders=[1, 0, 2, 3])
    pass