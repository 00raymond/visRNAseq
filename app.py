from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename
import os
import readqc

app = Flask(__name__)

UPLOAD_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# todo:
# implement analysis on referenced genome with Magic-BLAST (map RNA/DNA seq. against whole genome)
# test with placeholder FASTA file for plot PNG


@app.route('/plot/<filename>')
def serve_plot(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), mimetype='image/png')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'genome_file' not in request.files or 'seq_file' not in request.files:
            return render_template('file_failed.html', error='Missing file part')

        genome_file = request.files['genome_file']
        seq_file = request.files['seq_file']

        if genome_file.filename == '' or seq_file.filename == '':
            return render_template('file_failed.html', error='No selected file')

        if not (genome_file.filename.endswith('.fasta') or genome_file.filename.endswith('.fa')) or \
                not (seq_file.filename.endswith('.fastq') or seq_file.filename.endswith('.bam')):
            return render_template('file_failed.html', error='Invalid file format')

        print("passed file exam")
        genome_filename = secure_filename(genome_file.filename)
        seq_filename = secure_filename(seq_file.filename)
        genome_file.save(os.path.join(app.config['UPLOAD_FOLDER'], genome_filename))
        seq_file.save(os.path.join(app.config['UPLOAD_FOLDER'], seq_filename))

        print("files saved")

        seq_file_path = os.path.join(app.config['UPLOAD_FOLDER'], seq_filename)
        plot_file_path = readqc.quality_metrics(seq_file_path)

        return render_template('file_success.html', plot_file_path=plot_file_path)

    return render_template('upload_file.html')


@app.route('/')
def hello_world():
    return render_template('home.html')

    # todo:
    # input FASTQ file <done>
    # input genome reference file <done>
    # configure docker
    # implement FastQC for quality control(accepts FASTQ or BAM, generating summary graphs/tables) <done>


@app.route('/download')
def download_page():
    return "download"


if __name__ == '__main__':
    app.run()
