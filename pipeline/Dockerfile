# base Docker image that we will build on
#FROM python:3.13.11-slim

# set up our image by installing prerequisites; pandas in this case
#RUN pip install pandas pyarrow

# set up the working directory inside the container
#WORKDIR /code
# copy the script to the container. 1st name is source file, 2nd is destination
#COPY pipeline.py .

# define what to do first when the container runs
# in this example, we will just run the script
#ENTRYPOINT ["python", "pipeline.py"]
##############
# Start with slim Python 3.13 image
#FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
#COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
#WORKDIR /app


#ENV PATH="/app/.venv/bin:$PATH"


#COPY "pyproject.toml" "uv.lock" ".python-version" ./

#RUN uv sync --locked


#COPY pipeline.py pipeline.py


#ENTRYPOINT ["uv", "run", "python", "pipeline.py"]

# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"
COPY "pyproject.toml" "uv.lock" ".python-version" ./
RUN uv sync --locked
COPY pipeline.py pipeline.py
ENTRYPOINT ["python", "pipeline.py"]