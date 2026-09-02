FROM rust:1.81-bookworm

ARG KUJO_RUNTIME_REF=b1cec6b6c0f22e9015f5a8d3d1afc7e30b6964f7

RUN apt-get update \
	&& apt-get install -y --no-install-recommends git ca-certificates \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /opt/kujo-runtime

RUN git init /opt/kujo-runtime \
	&& git -C /opt/kujo-runtime remote add origin https://github.com/kujolang/kujo.git \
	&& git -C /opt/kujo-runtime fetch --depth 1 origin "$KUJO_RUNTIME_REF" \
	&& git -C /opt/kujo-runtime checkout --detach "$KUJO_RUNTIME_REF" \
	&& cargo build --release --locked --manifest-path /opt/kujo-runtime/Cargo.toml

ENV PATH="/opt/kujo-runtime/target/release:${PATH}"

WORKDIR /workspace

CMD ["kujo", "run", "main.kujo", "--interpreter", "serve"]
