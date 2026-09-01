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
		# Discard every client assertion before injecting values produced by the
		# identity-aware authentication layer.
		proxy_set_header X-Kujo-Claim-Iss $verified_jwt_iss;
		proxy_set_header X-Kujo-Claim-Aud $verified_jwt_aud;
		proxy_set_header X-Kujo-Claim-Exp $verified_jwt_exp;
		proxy_set_header X-Kujo-Claim-Sub $verified_jwt_sub;
		proxy_set_header X-Kujo-Claim-Role $verified_jwt_role;
		proxy_set_header X-Kujo-Claim-Namespace $verified_jwt_namespace;
		proxy_set_header X-Kujo-Role "";
		proxy_set_header X-Kujo-Namespace "";
		proxy_set_header X-Kujo-Proxy-Secret $kujo_proxy_secret;
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
		header_up -X-Kujo-Claim-Iss
		header_up -X-Kujo-Claim-Aud
		header_up -X-Kujo-Claim-Exp
		header_up -X-Kujo-Claim-Sub
		header_up -X-Kujo-Claim-Role
		header_up -X-Kujo-Claim-Namespace
		header_up -X-Kujo-Role
		header_up -X-Kujo-Namespace
		header_up -X-Kujo-Proxy-Secret
		header_up X-Forwarded-Proto https
		header_up X-Forwarded-Host {host}
		header_up X-Request-Id {http.request.id}
	}
}
```

The Caddy block above deliberately strips identity assertions. An
identity-aware handler must then add freshly verified claim values and
`X-Kujo-Proxy-Secret` before proxying; do not forward client values. Keep the
proxy secret in the platform secret manager, not in the Caddyfile. The Nginx
sample likewise assumes the `$verified_jwt_*` values and
`$kujo_proxy_secret` come from trusted authentication/secret modules.

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
- [ ] Proxy strips client-supplied forwarding, `x-kujo-claim-*`, RBAC, and proxy-attestation headers and sets only verified values.
- [ ] RAG `KUJO_RAG_API_TRUSTED_PROXY_IPS` contains only the real proxy peers and the proxy attestation secret matches.
- [ ] HSTS and secure headers are present on all API responses.
- [ ] `curl -I https://<host>/health` shows secure header baseline.
- [ ] Direct access to backend `:8787` is blocked from public networks.

## Operational Notes

- Keep `KUJO_RAG_ENV=production` and strict startup validation enabled.
- Prefer `api_auth_provider=jwt_proxy` behind an identity-aware gateway for enterprise edge deployments.
