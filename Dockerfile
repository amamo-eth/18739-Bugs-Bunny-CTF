# References base image by SHA to avoid drift. Python 3.12.
FROM python@sha256:2fba8e70a87bcc9f6edd20dda0a1d4adb32046d2acbca7361bc61da5a106a914 AS base

# Challenge metadata and artifacts go in /challenge
RUN mkdir /challenge && chmod 700 /challenge

# Copy all challenge files into /app
COPY oracle carrot_stage1.bin carrot_stage2.bin /app/
WORKDIR /app


FROM base AS challenge

WORKDIR /app

# cmgr injects FLAG automatically
ARG FLAG

# Store flag inside container
RUN echo "${FLAG}" > flag.txt

# Create artifacts archive for downloads
RUN tar czvf /challenge/artifacts.tar.gz carrot_stage1.bin carrot_stage2.bin && \
    echo "{\"flag\":\"$(cat flag.txt)\"}" > /challenge/metadata.json

# Keep container alive
CMD ["tail", "-f", "/dev/null"]
