FROM continuumio/miniconda3
WORKDIR /app

# Create a base conda env
RUN conda create -n codec-harness-env python=3.10

# Instruct Docker to run subsequent commands inside the new Conda environment
SHELL ["conda", "run", "-n", "codec-harness-env", "/bin/bash", "-c"]

# Install ffmpeg from conda-forge
RUN conda install -c conda-forge ffmpeg --yes

# Copy project files
COPY . .

# Install the package and its dependencies using pip
RUN pip install .

# Set the entrypoint to the command-line script created by the package
ENTRYPOINT ["codec-harness"]