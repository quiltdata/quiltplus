# QuiltPlus

## Next-generation API for Quilt Universal Data Collections

QuiltPlus provides an asychronous, object-oriented wrapper around the Quilt API.
In particular, it implements a resource-based architecture using Quilt+ URIs in
order to support the Universal Data Client [udc](https://github.com/data-yaml/udc).

## Installation

```bash
python3 -m pip install quiltplus
```

## Usage

```python
from quiltplus import QuiltPackage
import anyio

URI = "quilt+s3://quilt-example#package=examples/wellplates"

async def print_contents(uri: str):
    pkg = QuiltPackage.FromURI(URI)
    files = await pkg.list()
    print(files)

anyio.run(print_contents, URI)
```
