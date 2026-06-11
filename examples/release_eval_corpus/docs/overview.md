# Platform Overview

The retrieval platform is designed for multi-tenant enterprise search workloads.
Service-to-service traffic is authenticated with mTLS at the edge and short-lived JWTs between internal services.
Index isolation is enabled per tenant namespace and each namespace writes to a distinct index artifact path.
The default deployment target uses three stateless API replicas behind a reverse proxy.
