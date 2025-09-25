FROM python:3.11-slim-bookworm

ARG VERSION

COPY ./dist/onnigiri-${VERSION}-py3-none-any.whl /tmp/onnigiri-${VERSION}-py3-none-any.whl

RUN pip3 install --break-system-packages /tmp/onnigiri-${VERSION}-py3-none-any.whl

WORKDIR "/work"
ENTRYPOINT ["onnigiri"]
