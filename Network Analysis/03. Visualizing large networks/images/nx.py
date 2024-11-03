import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, axes = plt.subplots(1, 5, figsize=(12, 3))
    
    for i, (filename, title) in enumerate([
        ('nx_random', 'nx.random_layout'),
        ('nx_circular', 'nx.circular_layout'),
        ('nx_shell', 'nx.shell_layout'),
        ('nx_spectral', 'nx.spectral_layout'),
        ('nx_spring', 'nx.spring_layout'),
    ]):
        axes[i].imshow(plt.imread(f'../results/{filename}.png'))
        axes[i].set_title(title)
    
    for ax in axes: ax.axis('off')
    fig.tight_layout()
    plt.savefig('nx.png')
