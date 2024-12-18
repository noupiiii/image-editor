import asyncio
from PIL import Image
from io import BytesIO
import numpy as np
from typing import Tuple, List
from collections import Counter
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import base64

Image.MAX_IMAGE_PIXELS = None


async def extract_color_palette(image_data: bytes, n_colors: int) -> List[str]:
    """
    Asynchronously extracts the top `n_colors` from an image.
    """
    return await asyncio.to_thread(_extract_color_palette_sync, image_data, n_colors)


def _extract_color_palette_sync(image_data: bytes, n_colors: int) -> List[str]:

    image = Image.open(BytesIO(image_data)).convert("RGB")

    image = image.resize((150, 150), resample=Image.Resampling.LANCZOS)
    
    np_img = np.array(image)
    height, width, _ = np_img.shape
    np_img = np_img.reshape(height * width, 3)

    kmeans = KMeans(n_clusters=n_colors, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(np_img)

    counts = np.bincount(labels)
    sorted_cluster_indices = np.argsort(counts)[::-1]

    cluster_centers = kmeans.cluster_centers_[sorted_cluster_indices]

    hex_colors = []
    for center in cluster_centers:
        r, g, b = (int(round(c)) for c in center)
        hex_colors.append(f"#{r:02x}{g:02x}{b:02x}")

    return hex_colors

async def read_image_as_float(image_data: bytes) -> np.ndarray:
    """
    Asynchronously reads an image and converts it to a NumPy array of type float64.
    Values are normalized between 0 and 1.
    """
    return await asyncio.to_thread(_read_image_as_float_sync, image_data)


def _read_image_as_float_sync(image_data: bytes) -> np.ndarray:
    """
    Synchronous helper to read an image and convert it to NumPy array.
    """
    with Image.open(BytesIO(image_data)) as img:
        img = img.convert("RGB")
        return np.asarray(img, dtype=np.float64) / 255.0


async def cluster_image(image: np.ndarray, n_colors: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Asynchronously clusters an image with K-Means.
    """
    return await asyncio.to_thread(_cluster_image_sync, image, n_colors)


def _cluster_image_sync(image: np.ndarray, n_colors: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Synchronous helper to cluster an image using K-Means.
    """
    reshaped_image = image.reshape(-1, image.shape[-1])
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(reshaped_image)
    return kmeans.cluster_centers_, kmeans.labels_


async def transfer_colors_by_cluster(
    source_image: np.ndarray, target_image: np.ndarray, n_colors: int
) -> np.ndarray:
    """
    Asynchronously performs color transfer by clusters.
    """
    return await asyncio.to_thread(
        _transfer_colors_by_cluster_sync, source_image, target_image, n_colors
    )


def _transfer_colors_by_cluster_sync(
    source_image: np.ndarray, target_image: np.ndarray, n_colors: int
) -> np.ndarray:
    """
    Synchronous helper to perform color transfer by clusters.
    """
    clusters_source, _ = _cluster_image_sync(source_image, n_colors)
    clusters_target, labels_target = _cluster_image_sync(target_image, n_colors)

    mapping = _map_clusters_sync(clusters_target, clusters_source)
    remapped_clusters = np.array([clusters_source[map_[1]] for map_ in mapping])

    h, w, _ = target_image.shape
    return _recreate_image_sync(remapped_clusters, labels_target, w, h)


async def encode_image_to_base64(image: np.ndarray) -> str:
    """
    Asynchronously encodes a NumPy image into a base64 string.
    """
    return await asyncio.to_thread(_encode_image_to_base64_sync, image)


def _encode_image_to_base64_sync(image: np.ndarray) -> str:
    """
    Synchronous helper to encode an image to base64.
    """
    pil_image = Image.fromarray((image * 255).astype(np.uint8))
    buffer = BytesIO()
    pil_image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _map_clusters_sync(clusters1: np.ndarray, clusters2: np.ndarray) -> List[Tuple[int, int]]:
    """
    Synchronous helper to find mapping between clusters of two images.
    """
    distances = cdist(clusters1, clusters2)
    mapping = [(i, np.argmin(distances[i])) for i in range(len(clusters1))]
    return mapping


def _recreate_image_sync(
    codebook: np.ndarray, labels: np.ndarray, w: int, h: int
) -> np.ndarray:
    """
    Synchronous helper to reconstruct an image from clusters and labels.
    """
    return codebook[labels].reshape(h, w, -1)
