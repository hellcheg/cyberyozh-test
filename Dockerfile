FROM python:3.12-slim-bookworm AS base-builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./

# =====================================================================
FROM base-builder AS prod-builder
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

# =====================================================================
FROM base-builder AS test-builder
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# =====================================================================
FROM python:3.12-slim-bookworm AS base-runtime

WORKDIR /app

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown 8888:8888 /entrypoint.sh

RUN useradd -m -u 8888 app && chown app:app /app
USER app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

COPY --chown=app:app src/ .

# =====================================================================
FROM base-runtime AS runtime

COPY --from=prod-builder --chown=app:app /app/.venv /app/.venv

EXPOSE 8000
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# =====================================================================
FROM base-runtime AS test-runtime

COPY --from=test-builder --chown=app:app /app/.venv /app/.venv
COPY --chown=app:app pyproject.toml ./

ENTRYPOINT []
CMD ["pytest"]
