import matplotlib.pyplot as plt

if __name__ == '__main__':
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.5))
    
    for i, (filename, title) in enumerate([
        ('basic_grid', 'Grid'),
        ('basic_circle', 'Circle'),
        ('basic_spiral', 'Spiral'),
        ('basic_random', 'Random'),
    ]):
        axes[i].imshow(plt.imread(f'../results/{filename}.png'))
        axes[i].set_title(title)
    
    for ax in axes: ax.axis('off')
    fig.tight_layout()
    plt.savefig('basic.png')
