ARG PYTHON_VER=3.12

# build stage
FROM python:${PYTHON_VER}-alpine AS builder

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# copy project files
COPY pyproject.toml pdm.lock /app/
COPY src/ /app/src

# install dependencies and project into local packages directory
WORKDIR /app
RUN mkdir __pypackages__ \
    && pdm sync --prod --no-editable

# run stage
# TODO: use more secure Red Hat Universal Base Images (UBI) when available for python 3.12
FROM python:${PYTHON_VER}-alpine
ARG PYTHON_VER

# copy packages from build
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/${PYTHON_VER}/lib /app/pkgs

# Generate .opt-2.pyc files to speed up the time to import modules.
# Not possible to package pyc inside the wheel because pycwheel module is not available in python 3.
RUN python -OO -m compileall -j $(nproc) -x '.*(/tests?/.*|tests?.py)' /app/pkgs

# use .opt-2.pyc files of this repository created with compileall module
CMD ["python", "-BOOm", "back"]
