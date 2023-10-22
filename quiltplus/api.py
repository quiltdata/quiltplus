# Create FastAPI wrapper for quiltplus

from fastapi import FastAPI
from quiltplus.resource import QuiltResourceURI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello QuiltPlus!"}


@app.get("/registry/{registry_id}", status_code=200)
async def get_registry(registry_id: str):
    uri = f"quilt+s3://{registry_id}"
    return QuiltResourceURI(uri)


@app.get("/registry/{registry_id}/", status_code=200)
async def list_registry(registry_id: str):
    uri = f"quilt+s3://{registry_id}"
    registry = QuiltResourceURI(uri)
    return await registry.list()


@app.get("/registry/{registry_id}/package/{package_id}", status_code=200)
async def get_package(registry_id, package_id: str):
    package_name = package_id.replace("_", "/")
    uri = f"quilt+s3://{registry_id}#package={package_name}"
    return QuiltResourceURI(uri)


@app.get("/registry/{registry_id}/package/{package_id}/", status_code=200)
async def list_package(registry_id, package_id: str):
    package_name = package_id.replace("_", "/")
    uri = f"quilt+s3://{registry_id}#package={package_name}"
    pkg = QuiltResourceURI(uri)
    return await pkg.list()
