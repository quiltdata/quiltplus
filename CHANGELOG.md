# CHANGELOG

## 0.9.2 (2023-06-04)

- QuiltLocal._diff directory vs local registry
- QuiltPackage.diff => quilt+stage+{add,rm,touch}+URI
- properly return list of URIs from REST methods

## 0.9.1 (2023-06-03)

- support get, put, patch operations
- improve typing and test coverage (>95%)

## 0.9.0 (2023-05-29)

Pre-release to support Universal Data Client (udc) development.

- Rewrote QuiltResource to use attribute dictionaries
- Added QuiltType to identify resource types
- Added QuiltURI to parse and validate Quilt+ URIs, using UDC's "UnUri" parsing
- Split out QuiltLocal to manage local file storage and temporary directories
