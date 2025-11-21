FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

FROM base AS builder

WORKDIR /build

RUN pip install --no-cache-dir --user prometheus-client==0.19.0

FROM base AS runtime

ENV APPUSER=appuser \
    PATH=/home/appuser/.local/bin:$PATH

WORKDIR /app

RUN groupadd -r ${APPUSER} && \
    useradd -r -g ${APPUSER} -m -d /home/${APPUSER} ${APPUSER}

COPY --from=builder --chown=${APPUSER}:${APPUSER} /root/.local /home/${APPUSER}/.local

COPY --chown=${APPUSER}:${APPUSER} app.py /app/app.py

USER ${APPUSER}

EXPOSE 8000

LABEL description="Python app with Prometheus metrics for KEDA autoscaling"

CMD ["python", "-u", "/app/app.py"]