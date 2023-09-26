# visRNAseq
Visualization for raw RNA seq. fastq data (Quality Score Distribution, GC Content and Read Length)

*as of 9/26/2023, placeholder fasta formatted file is required to run

## How to Run

1. **Build the Docker Image:**
   ```sh
   docker build -t <image-name> .

2. **Run Docker Image:**
   ```sh
   docker run -p 5000:5000 <image-name>

3. **Access Application:**
   ```sh
   Open a web browser and navigate to http://localhost:5000

## Troubleshooting

### Port is Already Allocated

If you encounter an error like `Bind for 0.0.0.0:5000 failed: port is already allocated` when trying to run the container, another process is using port 5000.
To resolve this issue, you have a few options:

1. **Stop the Process Using Port 5000:**
   Identify and stop the process that is using port 5000. You can use the following command to find the process ID (PID) of the process using port 5000:
   ```sh
   lsof -i :5000
   kill -9 <PID>
   ```
   if a docker container is using it, you can do the following:
   ```sh
   docker ps
   docker stop <container_id_or_name>
   ```
   
3. **Use different port:**
   For example, using 5001 instead of 5000 and accessing it at localhost:5001
   ```sh
   docker run -p 5001:5000 <image-name>
