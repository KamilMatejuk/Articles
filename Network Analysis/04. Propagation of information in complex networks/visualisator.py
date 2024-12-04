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
    def generate_graph(ax: plt.Axes, graph: nx.Graph, graph_pos: np.ndarray = None):
        if graph_pos is None:
            graph_points_dict = nx.kamada_kawai_layout(graph)
            graph_pos = np.array([graph_points_dict[n] for n in graph.nodes])

        nodes_ids = list(graph.nodes)
        colors = [graph.nodes[n]['state'].value for n in graph.nodes]
        ax.scatter(graph_pos[:, 0], graph_pos[:, 1], zorder=2, c=colors, s=100)
        for e1, e2 in graph.edges:
            coordinates = np.array([graph_pos[nodes_ids.index(e1)], graph_pos[nodes_ids.index(e2)]])
            plt.plot(coordinates[:, 0], coordinates[:, 1], zorder=1, color='#999999', linewidth=2)
        ax.axis('off')
        ax.set_xticks([])
        ax.set_yticks([])
