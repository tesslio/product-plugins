# Repository rules

Every handler under `src/tenant/` must derive the tenant from authenticated
request context. A request field may never select the tenant for a read or write.
