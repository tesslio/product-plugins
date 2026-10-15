# Review a README change

Review this pull request and flag any findings that should be addressed. Write only actionable findings to `review.md`.

This repository is a small web service. It is not an agent plugin. Its `Makefile`, unchanged by this pull request, defines these targets:

```make
test:
	go test ./...

test-integration:
	go test -tags integration ./...

run:
	go run ./cmd/server
```

`cmd/server/config.go`, unchanged by this pull request, reads the port like this:

```go
port := os.Getenv("PORT")
if port == "" {
	port = "3000"
}
```

```diff
diff --git a/README.md b/README.md
--- a/README.md
+++ b/README.md
@@ -1,3 +1,13 @@
 # shortlink

 A URL shortener.
+
+## Getting started
+
+Run the service locally with `make run`. It listens on port 8080 unless you
+set `PORT`.
+
+Run the unit tests with `make test-unit`, and the integration tests, which
+need a local Postgres, with `make test-integration`.
+
+Pretty simple!
```
