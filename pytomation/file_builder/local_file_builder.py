import shutil
import uuid
from os import PathLike
from pathlib import Path
from typing import Callable

from .file_builder import FileBuilder, TmpDirectory


class LocalFileBuilder(FileBuilder):

    def __init__(self, workdir: PathLike, tmp_dir_name: str = '.module__cache'):
        self.mod_dir = Path(workdir).absolute()
        self.workdir = self.mod_dir / tmp_dir_name
        self.dir_name = tmp_dir_name

    def clean(self, name: str = None):
        if name is None:
            file = self.workdir
        else:
            file = self._get_tmp_file(name)

        if file.is_dir():
            shutil.rmtree(file)

    def exists(self, name: str) -> bool:
        return self._get_tmp_file(name).is_dir() and self._get_current_file(name).is_file()

    def file(self, name: str, build_hash: str, build_func: Callable[[Path], None]) -> Path:
        file = self._get_tmp_file(name)
        cached_file = file.joinpath(build_hash)

        if cached_file.is_file():
            return cached_file

        build_func(cached_file)

        self._update_current_file(name, build_hash)

        return cached_file

    def get_current(self, name: str) -> Path:
        return self._get_current_file(name)

    def get_file_path(self, name: str):
        return self.mod_dir.joinpath(name)

    def tmp_dir(self) -> TmpDirectory:
        random_name = uuid.uuid4().hex
        return LocalTmpDirectory(self, self.workdir / f'tmp_{random_name}', self.mod_dir)

    def _get_tmp_file(self, name: str):
        file_path = self.workdir.joinpath(name)

        file_path.mkdir(parents=True, exist_ok=True)

        return file_path

    def _update_current_file(self, name: str, build_hash: str):
        file = self._get_tmp_file(name)
        current_desc = file / '.current'

        if not current_desc.is_file():
            current_desc.touch()

        current_desc.write_text(build_hash)

    def _get_current_file(self, name: str) -> Path:
        file = self._get_tmp_file(name)
        current_desc = file / '.current'

        if not current_desc.is_file():
            raise FileNotFoundError(f'File {name} does not exist')

        current_hash = current_desc.read_text()

        current_file = file / current_hash

        if not current_file.is_file():
            raise FileNotFoundError(f'Cache in damage. Please, clean it')

        return current_file


class LocalTmpDirectory(TmpDirectory):

    def __init__(self, file_builder: FileBuilder, tmp_dir: str | Path, module_dir: str | Path):
        self.file_builder = file_builder
        self.tmp_dir = Path(tmp_dir)
        self.module_dir = Path(module_dir)

    @property
    def path(self) -> Path:
        return self.tmp_dir

    def copy(self, src: str, relative_path: str | Path = '.', dest_name: str = None) -> None:
        file_src = Path(src)

        if not file_src.is_file():
            raise FileNotFoundError(f'File {src} does not exist')

        self._copy_file(file_src, relative_path, (dest_name or file_src.name))

    def copy_from_cache(self, name: str, relative_path: str | Path = '.', dest_name: str = None) -> None:
        org_file = Path(name)
        file = self.file_builder.get_current(name)

        self._copy_file(file, relative_path, (dest_name or org_file.name))

    def copy_from_module(self, src: str, relative_path: str | Path = '.', dest_name: str = None) -> None:
        file_src = self.module_dir / src

        if not file_src.is_file():
            raise FileNotFoundError(f'File {src} does not exist')

        self._copy_file(file_src, relative_path, (dest_name or file_src.name))

    def _copy_file(self, src: Path, relative_path: str | Path, dest_name: str) -> None:
        dest = self.tmp_dir / relative_path / dest_name
        dir_dest = dest.parent

        if not dir_dest.is_dir():
            dir_dest.mkdir(parents=True)

        shutil.copyfile(src, dest)

    def create(self):
        self.tmp_dir.mkdir(parents=True)

    def cleanup(self):
        shutil.rmtree(self.tmp_dir)
