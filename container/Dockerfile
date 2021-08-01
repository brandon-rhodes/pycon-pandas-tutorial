FROM continuumio/miniconda3:4.9.2-alpine

RUN apk update
RUN apk add curl
RUN conda install --yes jupyter matplotlib pandas

WORKDIR /app
COPY . .

RUN cd build && /bin/sh BUILD.sh

EXPOSE 8888
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
