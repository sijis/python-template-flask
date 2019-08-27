ARG PACKAGE_DIR=/app
ARG WHEEL_DIR=/wheel

FROM python:3.7-slim as BUILD

ARG PACKAGE_DIR
ARG WHEEL_DIR

RUN apt update && apt install git -y

COPY . $PACKAGE_DIR/

RUN ["mkdir", "$WHEEL_DIR"]
RUN pip3 wheel \
    --wheel-dir $WHEEL_DIR \
    --requirement $PACKAGE_DIR/requirements.txt \
    $PACKAGE_DIR


FROM python:3.7-slim
LABEL maintainer sijis

ARG WHEEL_DIR

COPY --from=BUILD $WHEEL_DIR $WHEEL_DIR

RUN pip3 install \
    --no-index \
    --find-links $WHEEL_DIR \
    python_template_flask

COPY app /
COPY ./settings.yaml /
RUN chmod 755 /app
ENV FLASK_ENV=production
ENV DATABASE_URL=""
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "python_template_flask.app:APP"]
