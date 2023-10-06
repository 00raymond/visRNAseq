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
        action = request.form.get('action')

        genome_file = request.files.get('genome_file', None)
        seq_file = request.files.get('seq_file', None)

        if not seq_file or seq_file.filename == '':
            return render_template('file_failed.html', error='FASTQ file is required')

        if not (seq_file.filename.endswith('.fastq') or seq_file.filename.endswith('.bam')):
            return render_template('file_failed.html', error='Invalid FASTQ file format')

        if action == "Visualize FASTQ":
            seq_filename = secure_filename(seq_file.filename)
            seq_file.save(os.path.join(app.config['UPLOAD_FOLDER'], seq_filename))
            seq_file_path = os.path.join(app.config['UPLOAD_FOLDER'], seq_filename)
            plot_file_path = readqc.quality_metrics(seq_file_path)
            return render_template('file_success.html', plot_file_path=plot_file_path)

        if action == "Upload for IGV Visualization":
            if not genome_file or genome_file.filename == '':
                return render_template('file_failed.html', error='FASTA file is required for IGV visualization')

            if not (genome_file.filename.endswith('.fasta') or genome_file.filename.endswith('.fa')):
                return render_template('file_failed.html', error='Invalid FASTA file format')

            genome_filename = secure_filename(genome_file.filename)
            genome_file.save(os.path.join(app.config['UPLOAD_FOLDER'], genome_filename))
            seq_filename = secure_filename(seq_file.filename)
            seq_file.save(os.path.join(app.config['UPLOAD_FOLDER'], seq_filename))

            return render_template('igv_viewer.html', genome_filename=genome_filename, seq_filename=seq_filename)

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


@app.route('/igv_viewer/<genome_filename>/<seq_filename>')
def igv_viewer(genome_filename, seq_filename):
    genome_file_path = os.path.join(app.config['UPLOAD_FOLDER'], genome_filename)
    seq_file_path = os.path.join(app.config['UPLOAD_FOLDER'], seq_filename)

    # Set up IGV or do any other necessary processing here

    return render_template('igv_viewer.html', genome_file_path=genome_file_path, seq_file_path=seq_file_path)


if __name__ == '__main__':
    app.run()
