# CHANGELOG

## 0.9.7 (2023-10-22)

- QuiltCore 0.3.5
- Pass all tests
- Mockup FastAPI server

## 0.9.6 (2023-08-09)

- Start using QuiltCore instead of Quilt3
- Start with get
- Incomplete support for put

## 0.9.5 (2023-06-10)

- Embed package names in attr dict (for parsing)

## 0.9.4 (2023-06-08)

- Versions inherit from Package (so get/put work)

## 0.9.3 (2023-06-06)

- New UnYaml 0.3.0
- fallible flag
- get returns file: URIs

## 0.9.2 (2023-06-04)

- QuiltLocal._diff directory vs local registry
- QuiltPackage.diff => quilt+stage+{add,rm,touch}+URI
- properly return list of URIs from REST methods
- preliminary path support

## 0.9.1 (2023-06-03)

- support get, put, patch operations
- improve typing and test coverage (>95%)

## 0.9.0 (2023-05-29)

Pre-release to support Universal Data Client (udc) development.

- Rewrote QuiltResource to use attribute dictionaries
- Added QuiltType to identify resource types
- Added QuiltURI to parse and validate Quilt+ URIs, using UDC's "UnUri" parsing
- Split out QuiltLocal to manage local file storage and temporary directories
