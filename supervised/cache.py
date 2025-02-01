author = {
    "name": "Sameed Husain",
    "h_index": 11,
    "citations": 408,
    "interests": ["Computer vision", "Machine learning", "Deep neural netrworks"],
    "scholar_id": "uyxcO-YAAAAJ",
    "affiliation": "Lecturer in AI, University of Surrey",
    "picture_url": "https://scholar.google.com/citations?view_op=medium_photo&user=uyxcO-YAAAAJ",
}

papers = {
    "recent_papers": [
        {
            "year": 2025,
            "title": "NarrativeBridge: Enhancing Video Captioning with Causal-Temporal Narrative",
            "pub_url": "https://arxiv.org/abs/2406.06499",
            "abstract": "Existing video captioning benchmarks and models lack coherent representations of causal-temporal narrative, which is sequences of events linked through cause and effect, unfolding over time and driven by characters or agents. This lack of narrative restricts models' ability to generate text descriptions that capture the causal and temporal dynamics inherent in video content. To address this gap, we propose NarrativeBridge, an approach comprising of: (1) a novel Causal-Temporal Narrative (CTN) captions benchmark generated using a large language model and few-shot prompting, explicitly encoding cause-effect temporal relationships in video descriptions, evaluated automatically to ensure caption quality and relevance; and (2) a dedicated Cause-Effect Network (CEN) architecture with separate encoders for capturing cause and effect dynamics independently, enabling effective learning and generation of captions with causal-temporal narrative. Extensive experiments demonstrate that CEN is more accurate in articulating the causal and temporal aspects of video content than the second best model (GIT): 17.88 and 17.44 CIDEr on the MSVD and MSR-VTT datasets, respectively. The proposed framework understands and generates nuanced text descriptions with intricate causal-temporal narrative structures present in videos, addressing a critical limitation in video captioning. For project details, visit https://narrativebridge.github.io/.",
            "citations": 3,
            "eprint_url": None,
        },
        {
            "year": 2024,
            "title": "Attend-Fusion: Efficient Audio-Visual Fusion for Video Classification",
            "pub_url": "https://arxiv.org/abs/2408.14441",
            "abstract": "Exploiting both audio and visual modalities for video classification is a challenging task, as the existing methods require large model architectures, leading to high computational complexity and resource requirements. Smaller architectures, on the other hand, struggle to achieve optimal performance. In this paper, we propose Attend-Fusion, an audio-visual (AV) fusion approach that introduces a compact model architecture specifically designed to capture intricate audio-visual relationships in video data. Through extensive experiments on the challenging YouTube-8M dataset, we demonstrate that Attend-Fusion achieves an F1 score of 75.64\\% with only 72M parameters, which is comparable to the performance of larger baseline models such as Fully-Connected Late Fusion (75.96\\% F1 score, 341M parameters). Attend-Fusion achieves similar performance to the larger baseline model while reducing the model size by nearly 80\\%, highlighting its efficiency in terms of model complexity. Our work demonstrates that the Attend-Fusion model effectively combines audio and visual information for video classification, achieving competitive performance with significantly reduced model size. This approach opens new possibilities for deploying high-performance video understanding systems in resource-constrained environments across various applications.",
            "citations": 0,
            "eprint_url": None,
        },
    ],
    "most_cited_papers": [
        {
            "year": 2017,
            "title": "Improving large-scale image retrieval through robust aggregation of local descriptors",
            "pub_url": "https://ieeexplore.ieee.org/abstract/document/7577858/",
            "abstract": "Visual search and image retrieval underpin numerous applications, however the task is still challenging predominantly due to the variability of object appearance and ever increasing size of the databases, often exceeding billions of images. Prior art methods rely on aggregation of local scale-invariant descriptors, such as SIFT, via mechanisms including Bag of Visual Words (BoW), Vector of Locally Aggregated Descriptors (VLAD) and Fisher Vectors (FV). However, their performance is still short of what is required. This paper presents a novel method for deriving a compact and distinctive representation of image content called Robust Visual Descriptor with Whitening (RVD-W). It significantly advances the state of the art and delivers world-class performance. In our approach local descriptors are rank-assigned to multiple clusters. Residual vectors are then computed in each cluster, normalized using a direction …",
            "citations": 74,
            "eprint_url": None,
        },
        {
            "year": 2019,
            "title": "REMAP: Multi-layer entropy-guided pooling of dense CNN features for image retrieval",
            "pub_url": "https://ieeexplore.ieee.org/abstract/document/8720226/",
            "abstract": "This paper addresses the problem of very large-scale image retrieval, focusing on improving its accuracy and robustness. We target enhanced robustness of search to factors, such as variations in illumination, object appearance and scale, partial occlusions, and cluttered backgrounds-particularly important when a search is performed across very large datasets with significant variability. We propose a novel CNN-based global descriptor, called REMAP, which learns and aggregates a hierarchy of deep features from multiple CNN layers, and is trained end-to-end with a triplet loss. REMAP explicitly learns discriminative features which are mutually supportive and complementary at various semantic levels of visual abstraction. These dense local features are max-pooled spatially at each layer, within multi-scale overlapping regions, before aggregation into a single image-level descriptor. To identify the semantically …",
            "citations": 60,
            "eprint_url": None,
        },
    ],
}
