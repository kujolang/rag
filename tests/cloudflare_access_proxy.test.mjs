import assert from "node:assert/strict";
import { generateKeyPairSync, sign } from "node:crypto";
import test from "node:test";

import {
  ProxyError,
  buildUpstreamHeaders,
  resolveIdentity,
  verifyAccessJwt,
} from "../deploy/cloudflare/access_proxy.mjs";

const { privateKey, publicKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const publicJwk = publicKey.export({ format: "jwk" });
publicJwk.kid = "test-key";
publicJwk.alg = "RS256";
publicJwk.use = "sig";

function token(claims, header = { alg: "RS256", kid: "test-key", typ: "JWT" }) {
  const encodedHeader = Buffer.from(JSON.stringify(header)).toString("base64url");
  const encodedClaims = Buffer.from(JSON.stringify(claims)).toString("base64url");
  const signature = sign("RSA-SHA256", Buffer.from(`${encodedHeader}.${encodedClaims}`), privateKey);
  return `${encodedHeader}.${encodedClaims}.${signature.toString("base64url")}`;
}

const baseClaims = {
  iss: "https://team.cloudflareaccess.com",
  aud: ["staging-audience"],
  exp: 2_000,
  nbf: 900,
  sub: "subject-1",
  email: "tester@example.test",
};

const options = {
  audience: "staging-audience",
  clockSkewSeconds: 0,
  fetchImpl: async () => new Response(JSON.stringify({ keys: [publicJwk] })),
  issuer: "https://team.cloudflareaccess.com",
  jwksUrl: "https://team.cloudflareaccess.com/cdn-cgi/access/certs",
  nowSeconds: 1_000,
};

test("accepts a correctly signed and bounded Cloudflare Access token", async () => {
  const claims = await verifyAccessJwt(token(baseClaims), options);
  assert.equal(claims.sub, "subject-1");
});

test("accepts a signed service-token identity only through an explicit mapping key", async () => {
  const claims = await verifyAccessJwt(token({ ...baseClaims, sub: "", email: undefined, common_name: "service.access" }), options);
  assert.equal(claims.verified_subject, "service.access");
  assert.deepEqual(resolveIdentity(claims, { "service.access": { role: "reader", namespace: "staging" } }), {
    role: "reader",
    namespace: "staging",
  });
});

test("rejects unsupported algorithms, wrong audiences, expiry, and JWKS failure", async () => {
  await assert.rejects(() => verifyAccessJwt(token(baseClaims, { alg: "HS256", kid: "test-key" }), options), ProxyError);
  await assert.rejects(() => verifyAccessJwt(token({ ...baseClaims, aud: "wrong" }), options), ProxyError);
  await assert.rejects(() => verifyAccessJwt(token({ ...baseClaims, exp: 999 }), options), ProxyError);
  const corrupted = `${token(baseClaims).slice(0, -1)}A`;
  await assert.rejects(() => verifyAccessJwt(corrupted, options), ProxyError);
  await assert.rejects(
    () => verifyAccessJwt(token(baseClaims), { ...options, fetchImpl: async () => { throw new Error("offline"); } }),
    (error) => error.code === "jwks_unavailable",
  );
});

test("uses only explicit identity mappings", () => {
  const mapping = { "tester@example.test": { role: "reader", namespace: "staging" } };
  assert.deepEqual(resolveIdentity(baseClaims, mapping), { role: "reader", namespace: "staging" });
  assert.throws(() => resolveIdentity({ ...baseClaims, email: "unknown@example.test" }, mapping), /no approved Kujo role/);
});

test("strips spoofable identity headers and rebuilds verified values", () => {
  const headers = buildUpstreamHeaders({
    "content-type": "application/json",
    "cf-access-jwt-assertion": "secret-token",
    "x-kujo-claim-role": "admin",
    "x-kujo-namespace": "other",
    "x-forwarded-for": "203.0.113.4",
  }, baseClaims, { role: "reader", namespace: "staging" }, "proxy-secret");
  assert.equal(headers.get("content-type"), "application/json");
  assert.equal(headers.get("cf-access-jwt-assertion"), null);
  assert.equal(headers.get("x-forwarded-for"), null);
  assert.match(headers.get("x-kujo-claim-sub"), /^sha256:[0-9a-f]{64}$/);
  assert.equal(headers.get("x-kujo-claim-sub").includes("subject-1"), false);
  assert.equal(headers.get("x-kujo-claim-role"), "reader");
  assert.equal(headers.get("x-kujo-claim-namespace"), "staging");
  assert.equal(headers.get("x-kujo-proxy-secret"), "proxy-secret");
});
