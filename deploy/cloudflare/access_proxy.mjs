import { createHash, createPublicKey, randomUUID, verify as verifySignature } from "node:crypto";
import { createServer } from "node:http";

const IDENTITY_HEADERS = new Set([
  "authorization",
  "cookie",
  "cf-access-jwt-assertion",
  "x-kujo-claim-iss",
  "x-kujo-claim-aud",
  "x-kujo-claim-exp",
  "x-kujo-claim-sub",
  "x-kujo-claim-role",
  "x-kujo-claim-namespace",
  "x-kujo-role",
  "x-kujo-namespace",
  "x-kujo-proxy-secret",
  "x-forwarded-for",
  "x-forwarded-host",
  "x-forwarded-proto",
  "forwarded",
]);

const FORWARDED_HEADERS = new Set([
  "accept",
  "content-type",
  "x-idempotency-key",
  "x-request-id",
]);

function decodeJsonSegment(segment, label) {
  try {
    return JSON.parse(Buffer.from(segment, "base64url").toString("utf8"));
  } catch {
    throw new ProxyError(401, "invalid_access_token", `Invalid JWT ${label}.`);
  }
}

function audienceIncludes(actual, expected) {
  if (typeof actual === "string") return actual === expected;
  return Array.isArray(actual) && actual.some((value) => value === expected);
}

function numericDate(value) {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

export class ProxyError extends Error {
  constructor(status, code, message) {
    super(message);
    this.status = status;
    this.code = code;
  }
}

export async function verifyAccessJwt(token, options) {
  if (typeof token !== "string" || token.length === 0 || token.length > 16_384) {
    throw new ProxyError(401, "missing_access_token", "A bounded Access JWT is required.");
  }

  const parts = token.split(".");
  if (parts.length !== 3 || parts.some((part) => part.length === 0)) {
    throw new ProxyError(401, "invalid_access_token", "Access JWT must have three segments.");
  }

  const header = decodeJsonSegment(parts[0], "header");
  const claims = decodeJsonSegment(parts[1], "payload");
  if (header.alg !== "RS256" || typeof header.kid !== "string" || header.kid.length === 0) {
    throw new ProxyError(401, "unsupported_access_token", "Access JWT must use an identified RS256 key.");
  }

  let response;
  try {
    response = await options.fetchImpl(options.jwksUrl, {
      headers: { accept: "application/json" },
      redirect: "error",
      signal: AbortSignal.timeout(options.jwksTimeoutMs ?? 5_000),
    });
  } catch {
    throw new ProxyError(503, "jwks_unavailable", "Access JWKS could not be retrieved.");
  }
  if (!response.ok) {
    throw new ProxyError(503, "jwks_unavailable", "Access JWKS returned a non-success response.");
  }

  let jwks;
  try {
    jwks = await response.json();
  } catch {
    throw new ProxyError(503, "jwks_invalid", "Access JWKS was not valid JSON.");
  }
  const key = Array.isArray(jwks?.keys)
    ? jwks.keys.find((candidate) => candidate?.kid === header.kid && candidate?.kty === "RSA")
    : null;
  if (!key) {
    throw new ProxyError(401, "unknown_access_key", "Access JWT signing key was not found.");
  }

  let verified = false;
  try {
    verified = verifySignature(
      "RSA-SHA256",
      Buffer.from(`${parts[0]}.${parts[1]}`),
      createPublicKey({ key, format: "jwk" }),
      Buffer.from(parts[2], "base64url"),
    );
  } catch {
    verified = false;
  }
  if (!verified) {
    throw new ProxyError(401, "invalid_access_signature", "Access JWT signature verification failed.");
  }

  const now = options.nowSeconds ?? Math.floor(Date.now() / 1_000);
  const skew = options.clockSkewSeconds ?? 30;
  const exp = numericDate(claims.exp);
  const nbf = claims.nbf === undefined ? null : numericDate(claims.nbf);
  if (claims.iss !== options.issuer || !audienceIncludes(claims.aud, options.audience)) {
    throw new ProxyError(401, "invalid_access_claims", "Access JWT issuer or audience is invalid.");
  }
  if (exp === null || exp <= now - skew || (claims.nbf !== undefined && (nbf === null || nbf > now + skew))) {
    throw new ProxyError(401, "invalid_access_time", "Access JWT is expired or not yet valid.");
  }
  const subject = typeof claims.sub === "string" && claims.sub.length > 0
    ? claims.sub
    : claims.common_name;
  if (typeof subject !== "string" || subject.length === 0) {
    throw new ProxyError(401, "invalid_access_subject", "Access JWT user or service-token subject is required.");
  }
  claims.verified_subject = subject;
  return claims;
}

export function resolveIdentity(claims, identityMap) {
  const email = typeof claims.email === "string" ? claims.email.trim().toLowerCase() : "";
  const entry = identityMap[email] ?? identityMap[claims.verified_subject ?? claims.sub];
  if (!entry || !["reader", "writer", "admin"].includes(entry.role)) {
    throw new ProxyError(403, "identity_not_mapped", "Authenticated identity has no approved Kujo role.");
  }
  if (typeof entry.namespace !== "string" || !/^[a-z0-9][a-z0-9_-]{0,63}$/.test(entry.namespace)) {
    throw new ProxyError(500, "invalid_identity_mapping", "Configured Kujo namespace is invalid.");
  }
  return { role: entry.role, namespace: entry.namespace };
}

export function buildUpstreamHeaders(incomingHeaders, claims, identity, proxySecret) {
  const headers = new Headers();
  for (const [name, value] of Object.entries(incomingHeaders)) {
    const lower = name.toLowerCase();
    if (IDENTITY_HEADERS.has(lower) || !FORWARDED_HEADERS.has(lower) || value === undefined) continue;
    headers.set(lower, Array.isArray(value) ? value.join(",") : String(value));
  }
  headers.set("x-request-id", headers.get("x-request-id") || randomUUID());
  // The current Kujo HTTP runtime handles one request per origin connection.
  // Close each verifier-to-origin hop so a pooled idle socket cannot block the
  // next request until the upstream timeout expires.
  headers.set("connection", "close");
  // Kujo's jwt_proxy contract requires a non-empty Bearer envelope before it
  // evaluates the trusted peer, proxy attestation, and verified claims. Never
  // forward the client's credential; synthesize a non-secret marker instead.
  headers.set("authorization", "Bearer cloudflare-access-verified");
  headers.set("x-kujo-proxy-secret", proxySecret);
  headers.set("x-kujo-claim-iss", claims.iss);
  headers.set("x-kujo-claim-aud", Array.isArray(claims.aud) ? claims.aud.join(",") : claims.aud);
  headers.set("x-kujo-claim-exp", String(claims.exp));
  const verifiedSubject = claims.verified_subject ?? claims.sub;
  const pseudonymousSubject = createHash("sha256").update(`kujo-rag:${verifiedSubject}`).digest("hex");
  headers.set("x-kujo-claim-sub", `sha256:${pseudonymousSubject}`);
  headers.set("x-kujo-claim-role", identity.role);
  headers.set("x-kujo-claim-namespace", identity.namespace);
  return headers;
}

async function readBoundedBody(request, maxBytes) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > maxBytes) throw new ProxyError(413, "request_too_large", "Request body exceeds the proxy limit.");
    chunks.push(chunk);
  }
  return chunks.length === 0 ? undefined : Buffer.concat(chunks);
}

async function readBoundedResponse(response, maxBytes) {
  const declared = Number(response.headers.get("content-length"));
  if (Number.isFinite(declared) && declared > maxBytes) {
    throw new ProxyError(502, "upstream_response_too_large", "Upstream response exceeds the proxy limit.");
  }
  if (!response.body) return Buffer.alloc(0);
  const chunks = [];
  let size = 0;
  for await (const chunk of response.body) {
    size += chunk.length;
    if (size > maxBytes) throw new ProxyError(502, "upstream_response_too_large", "Upstream response exceeds the proxy limit.");
    chunks.push(chunk);
  }
  return Buffer.concat(chunks);
}

function sendError(response, error) {
  const status = error instanceof ProxyError ? error.status : 502;
  const code = error instanceof ProxyError ? error.code : "proxy_failure";
  response.writeHead(status, { "content-type": "application/json", "cache-control": "no-store" });
  response.end(JSON.stringify({ ok: false, error: code }));
}

export function createAccessProxyServer(config) {
  return createServer(async (request, response) => {
    try {
      if (!config.allowedMethods.includes(request.method)) {
        throw new ProxyError(405, "method_not_allowed", "HTTP method is not allowed.");
      }
      const tokenHeader = request.headers["cf-access-jwt-assertion"];
      const token = Array.isArray(tokenHeader) ? tokenHeader[0] : tokenHeader;
      const claims = await verifyAccessJwt(token, config);
      const identity = resolveIdentity(claims, config.identityMap);
      const body = await readBoundedBody(request, config.maxBodyBytes);
      const headers = buildUpstreamHeaders(request.headers, claims, identity, config.proxySecret);
      const target = new URL(request.url, config.upstreamUrl);
      if (target.origin !== new URL(config.upstreamUrl).origin) {
        throw new ProxyError(400, "invalid_target", "Proxy target is invalid.");
      }
      const upstream = await config.fetchImpl(target, {
        method: request.method,
        headers,
        body,
        redirect: "manual",
        signal: AbortSignal.timeout(config.upstreamTimeoutMs),
      });
      // Buffer and enforce the response limit before committing headers. If
      // the upstream stream fails or exceeds the bound, sendError can still
      // return a deterministic JSON error instead of resetting the client.
      const responseBody = await readBoundedResponse(upstream, config.maxResponseBytes);
      const responseHeaders = {
        "content-type": upstream.headers.get("content-type") || "application/octet-stream",
        "cache-control": "no-store",
        "x-content-type-options": "nosniff",
        "referrer-policy": "no-referrer",
      };
      response.writeHead(upstream.status, responseHeaders);
      response.end(responseBody);
    } catch (error) {
      sendError(response, error);
    }
  });
}

export function configFromEnvironment(env = process.env) {
  const teamDomain = env.CLOUDFLARE_ACCESS_TEAM_DOMAIN?.trim();
  const audience = env.CLOUDFLARE_ACCESS_AUDIENCE?.trim();
  const proxySecret = env.KUJO_RAG_API_TRUSTED_PROXY_SECRET?.trim();
  if (!teamDomain || !audience || !proxySecret) throw new Error("Required proxy configuration is missing.");
  let identityMap;
  try {
    identityMap = JSON.parse(env.KUJO_RAG_PROXY_IDENTITY_MAP_JSON || "{}");
  } catch {
    throw new Error("KUJO_RAG_PROXY_IDENTITY_MAP_JSON must be valid JSON.");
  }
  const issuer = `https://${teamDomain}`;
  return {
    allowedMethods: ["GET", "POST"],
    audience,
    clockSkewSeconds: 30,
    fetchImpl: fetch,
    identityMap,
    issuer,
    jwksTimeoutMs: 5_000,
    jwksUrl: `${issuer}/cdn-cgi/access/certs`,
    maxBodyBytes: 1_048_576,
    maxResponseBytes: 4_194_304,
    proxySecret,
    upstreamTimeoutMs: 20_000,
    upstreamUrl: "http://127.0.0.1:8787",
  };
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const server = createAccessProxyServer(configFromEnvironment());
  server.headersTimeout = 5_000;
  server.requestTimeout = 20_000;
  server.keepAliveTimeout = 5_000;
  server.listen(8080, "127.0.0.1");
}
