# TLS And Reverse Proxy Hardening

This guide defines a production deployment path where Kujo RAG runs on a private interface and TLS is terminated at a reverse proxy.

## Threat Model Baseline

- Never expose the Kujo RAG API directly on a public interface without TLS termination.
- Keep Kujo RAG bound to loopback or private network interfaces (`127.0.0.1` or RFC1918 ranges).
- Treat proxy identity headers as untrusted unless injected by your own edge proxy.

## Deployment Patterns

### Edge TLS Termination (Recommended)

1. Public traffic terminates TLS at a hardened edge proxy.
2. Proxy forwards traffic to Kujo RAG over private network only.
3. Proxy injects forwarding headers and strips incoming user-supplied forwarding headers.

### Internal TLS (High-Assurance)

1. Keep edge TLS termination.
2. Add mTLS or internal TLS between proxy and Kujo RAG network segment when required by policy.
3. Restrict backend access with firewall rules and service identity controls.

## Nginx Sample

```nginx
server {
	listen 443 ssl http2;
	server_name rag.example.com;

	ssl_protocols TLSv1.2 TLSv1.3;
	ssl_prefer_server_ciphers on;

	add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
	add_header X-Content-Type-Options "nosniff" always;
	add_header X-Frame-Options "DENY" always;
	add_header Referrer-Policy "no-referrer" always;
	add_header Content-Security-Policy "default-src 'none'; frame-ancestors 'none'; base-uri 'none'" always;

	location / {
		proxy_pass http://127.0.0.1:8787;
		proxy_http_version 1.1;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-Proto https;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Forwarded-Host $host;
		proxy_set_header X-Request-Id $request_id;
		proxy_set_header Connection "";
	}
}
```

## Caddy Sample

```caddy
rag.example.com {
	header {
		Strict-Transport-Security "max-age=31536000; includeSubDomains"
		X-Content-Type-Options "nosniff"
		X-Frame-Options "DENY"
		Referrer-Policy "no-referrer"
		Content-Security-Policy "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
	}

	reverse_proxy 127.0.0.1:8787 {
		header_up X-Forwarded-Proto https
		header_up X-Forwarded-Host {host}
		header_up X-Request-Id {http.request.id}
	}
}
```

## Secure Header Baseline

At minimum, enforce these headers at the proxy layer:

- `Strict-Transport-Security`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: no-referrer`
- `Content-Security-Policy` with restrictive defaults

## Deployment Checklist (Validation)

Use this checklist before production promotion:

- [ ] Kujo RAG process is bound to non-public interface (`127.0.0.1` or private subnet).
- [ ] TLS certificates are valid and auto-renewal is configured.
- [ ] TLS 1.2+ is enforced; weak protocols/ciphers are disabled.
- [ ] Proxy strips client-supplied forwarding headers and sets trusted values.
- [ ] HSTS and secure headers are present on all API responses.
- [ ] `curl -I https://<host>/health` shows secure header baseline.
- [ ] Direct access to backend `:8787` is blocked from public networks.

## Operational Notes

- Keep `KUJO_RAG_ENV=production` and strict startup validation enabled.
- Prefer `api_auth_provider=jwt_proxy` behind an identity-aware gateway for enterprise edge deployments.
