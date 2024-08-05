import functools
import hashlib
import json
import shutil
from abc import abstractmethod
from pathlib import Path
from typing import Callable


class FileBuilder:

    @abstractmethod
    def file(
        self, name: str, build_hash: str, build_func: Callable[[Path], None]
    ) -> Path:
        pass

    @abstractmethod
    def get_current(self, name: str) -> Path:
        pass

    @abstractmethod
    def clean(self, name: str = None):
        pass

    @abstractmethod
    def exists(self, name: str) -> bool:
        pass

    @abstractmethod
    def get_file_path(self, name: str) -> Path:
        pass

    @abstractmethod
    def tmp_dir(self) -> "TmpDirectory":
        pass

    def file_from_template(
        self,
        name: str,
        template: Path | str,
        build_func: Callable,
        template_ctx: any = None,
    ) -> Path:

        if isinstance(template, str):
            template = self.get_file_path(template)

        if not template.is_file():
            raise FileNotFoundError(f"Template file {template} does not exist")

        with template.open(mode="rb") as f:
            tmpl_hash = hashlib.file_digest(f, "md5").hexdigest()

        if template_ctx is not None:
            json_str = json.dumps(template_ctx)
            ctx_json = hashlib.md5(json_str.encode()).hexdigest()
            tmpl_hash = f"{tmpl_hash}:{ctx_json}"

        build_func = functools.partial(
            build_func, template=template, context=template_ctx
        )

        return self.file(name, tmpl_hash, build_func)


class TmpDirectory:

    @property
    @abstractmethod
    def path(self) -> Path:
        pass

    @abstractmethod
    def copy(
        self, src: str, relative_path: str | Path = ".", dest_name: str = None
    ) -> None:
        pass

    @abstractmethod
    def copy_from_cache(
        self, name: str, relative_path: str | Path = ".", dest_name: str = None
    ) -> None:
        pass

    @abstractmethod
    def copy_from_module(
        self, src: str, relative_path: str | Path = ".", dest_name: str = None
    ) -> None:
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def cleanup(self):
        pass

    def mkdir(self, rel_path: str | Path) -> Path:
        new_dir = Path(self.path / rel_path)
        new_dir.mkdir(parents=True)
        return new_dir

    def move(self, src: str, dest: str):
        shutil.move(self.path / src, self.path / dest)

    def __enter__(self):
        self.create()
        return self

    def __exit__(self, *args, **kwargs):
        self.cleanup()
