from importlib.resources import as_file, files, Package

from clvm_rs import Program


try:
    from runtime_builder import build_on_demand
except ImportError:
    # `runtime_builder` is an optional dependency for development only
    def build_on_demand(*args):
        pass


def load_resource(
    package: Package,
    resource_path: str,
) -> bytes:
    build_on_demand(package, resource_path)
    with as_file(files(package).joinpath(resource_path)) as target_path:
        return target_path.read_bytes()


def load_program(
    package: Package,
    resource_path: str,
) -> Program:
    """
    package: a package identifier (often `__package__` for "this package"
        or a dotted string "foo.bar")
    resource_path: a `.hex` resource file in that package

    If the `chialisp_builder` wheel is installed, it will be used to rebuild
    the `.hex` file on demand prior to it being returned to optimize the
    develop/test cycle.
    """
    return Program.fromhex(load_resource(package, resource_path).decode("utf8"))
