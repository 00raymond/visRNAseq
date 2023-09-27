import os
import random
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO


def quality_metrics(fastq_file, sampling_fraction=0.01):
    quality_scores_bin = [0] * 42
    gc_contents = []
    read_lengths = []

    # iterate through each sequence
    for r in SeqIO.parse(fastq_file, "fastq"):
        if random.random() < sampling_fraction:
            # Quality score distribution
            for score in r.letter_annotations["phred_quality"]:
                quality_scores_bin[min(score, 41)] += 1

            # GC content calculation
            gc_content = (r.seq.count('G') + r.seq.count('C')) / len(r.seq) * 100
            gc_contents.append(gc_content)

            read_lengths.append(len(r.seq))

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 2, 1)
    plt.bar(range(42), quality_scores_bin, alpha=0.75)
    plt.title('Base Quality Score Distribution')
    plt.xlabel('Quality Score')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 2)
    plt.hist(gc_contents, bins=np.linspace(0, 100, 21), alpha=0.75)
    plt.title('GC Content Distribution')
    plt.xlabel('GC Content (%)')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 3)
    plt.hist(read_lengths, bins=np.linspace(0, max(read_lengths, default=1), 21), alpha=0.75)
    plt.title('Read Length Distribution')
    plt.xlabel('Read Length')
    plt.ylabel('Frequency')

    path_to_save = os.path.join('/app/app', 'static')

    plt.tight_layout()
    plot_file_path = os.path.join(path_to_save, 'quality_metrics.png')
    plt.savefig(plot_file_path)
    plt.close()

    return plot_file_path
