<template>
  <div class="">
    <h1 class="my-6 text-4xl font-bold">Explore the code of this application</h1>
    <p>The code you're about to see was written by Louis Bruche (noupiiii). This code doesn't detail the operation of the application itself, but rather the mathematical functions applied to the images.</p>
    
    <h2 class="text-xl font-semibold mt-6">Read images as float</h2>
    <p>This function reads data from an image.</p>
    <EmbedCode :code-snippet="codeSnipet_ReadImageAsFloat" />
    
    <h2 class="text-xl font-semibold mt-6">Cluster Image</h2>
    <p>This function extracts the color palette from an image. The function used returns the x dominant colors.</p>
    <EmbedCode :code-snippet="codeSnipet_ClusterImage" />

    <h2 class="text-xl font-semibold mt-6">Transfert image</h2>
    <p>This function transfers color from one image to another.</p>
    <EmbedCode :code-snippet="codeSnipet_TransfertColors" />

    <h2 class="text-xl font-semibold mt-6">Encode imae base64</h2>
    <p>To send the image faster over HTTP, we encode it in base 64.</p>
    <EmbedCode :code-snippet="codeSnipet_TransfertColors" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import EmbedCode from '~/components/embed-code.vue'

const codeSnipet_TransfertColors = ref(`
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
`)

const codeSnipet_ClusterImage = ref(`
def _cluster_image_sync(image: np.ndarray, n_colors: int) -> Tuple[np.ndarray, np.ndarray]:
    """
    Synchronous helper to cluster an image using K-Means.
    """
    reshaped_image = image.reshape(-1, image.shape[-1])
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(reshaped_image)
    return kmeans.cluster_centers_, kmeans.labels_
`)

const codeSnipet_ReadImageAsFloat = ref(`
def _read_image_as_float_sync(image_data: bytes) -> np.ndarray:
    """
    Synchronous helper to read an image and convert it to NumPy array.
    """
    with Image.open(BytesIO(image_data)) as img:
        img = img.convert("RGB")
        return np.asarray(img, dtype=np.float64) / 255.0
`)

const codeSnipet_ColorPalette = ref(`
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
`)
</script>
