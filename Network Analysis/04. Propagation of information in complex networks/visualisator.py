import imageio
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class Visualisator:

    @classmethod
    @staticmethod
    def generate_gif(images: list[np.ndarray], path: str, duration_ms: int, reverse: bool = False, interpolate_frames: int = 0):
        if reverse:
            images.extend(image.copy() for image in reversed(images[1:-1]))
        else:
            images.append(images[-1].copy())

        if interpolate_frames > 0:
            interpolated = []
            for image1, image2 in zip(images[:-1], images[1:]):
                interpolated.extend(Visualisator.interpolate(image1, image2, interpolate_frames))
            images = interpolated
            duration_ms /= (interpolate_frames + 1)

        imageio.mimsave(path, images, loop=0, duration=duration_ms)

    @classmethod
    @staticmethod
    def interpolate(image1: np.ndarray, image2: np.ndarray, frames: int) -> list[np.ndarray]:
        frames += 1
        interpolated = []
        for i in range(frames):
            alpha = (frames - i) / frames
            blended_image = image1.astype(np.float32) * alpha + image2.astype(np.float32) * (1-alpha)
            blended_image = np.clip(blended_image, 0, 255).astype(np.uint8)
            interpolated.append(blended_image)
        return [image1] + interpolated + [image2]
    
    @classmethod
    @staticmethod
    def generate_graph(ax: plt.Axes, graph: nx.Graph, graph_pos: np.ndarray = None,
                       node_kwargs: dict = None, edge_kwargs: dict = None, labels: list[str] = None):
        if graph_pos is None:
            graph_points_dict = nx.kamada_kawai_layout(graph)
            graph_pos = np.array([graph_points_dict[n] for n in graph.nodes])

        if node_kwargs is None:
            node_kwargs = {}
        if edge_kwargs is None:
            edge_kwargs = {}

        nodes_ids = list(graph.nodes)
        colors = [graph.nodes[n]['state'].value for n in graph.nodes]
        ax.scatter(graph_pos[:, 0], graph_pos[:, 1], zorder=2, c=colors, **node_kwargs)
        if labels is not None:
            for node, label in zip(nodes_ids, labels):
                ax.text(*graph_pos[nodes_ids.index(node)], label, zorder=3, color='black', va='center', ha='center')
        for e1, e2 in graph.edges:
            coordinates = np.array([graph_pos[nodes_ids.index(e1)], graph_pos[nodes_ids.index(e2)]])
            ax.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color='#999999', **edge_kwargs)
        ax.axis('off')

    @classmethod
    @staticmethod
    def draw_arrow(ax: plt.Axes):
        ax.plot([0, 1, 0.8, 1, 0.8], [0.5, 0.5, 1, 0.5, 0], linewidth=3, color='black')
        ax.axis('off')
        ax.set_xlim(-0.5, 1.5)
        ax.set_ylim(-5, 5)
