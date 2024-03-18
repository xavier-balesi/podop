ARG PYTHON_VER=3.12

# build stage
FROM python:${PYTHON_VER} AS builder

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
FROM python:${PYTHON_VER}
ARG PYTHON_VER

# copy packages from build
ENV PYTHONPATH=/app/pkgs
COPY --from=builder /app/__pypackages__/${PYTHON_VER}/lib /app/pkgs

# copy executables
COPY --from=builder /app/__pypackages__/${PYTHON_VER}/bin/* /bin/

CMD ["python", "-m", "back"]
