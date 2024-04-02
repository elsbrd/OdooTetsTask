import base64
import os
from enum import Enum
from functools import cached_property
from typing import List, Tuple, Optional

from odoo import models, fields, api, tools
from odoo.exceptions import UserError


FILE_STORAGE_DIR = "/var/lib/odoo/files/"
os.makedirs(FILE_STORAGE_DIR, exist_ok=True)


class StorageType(Enum):
    DATABASE = "db"
    DISK = "disk"

    @classmethod
    def to_selection_params(cls) -> List[Tuple[str, str]]:
        """Transforms enum members into a format suitable for Odoo selection fields."""
        return [(member.value, member.name.capitalize()) for member in cls]


class FileManager(models.Model):
    _name = "file.manager"
    _description = "File Manager"

    name = fields.Char("Name")
    file_data = fields.Binary("File", attachment=True)
    file_path = fields.Char("File Path", readonly=True)
    storage_type = fields.Selection(
        StorageType.to_selection_params(),
        string="Storage Type",
        default=StorageType.DATABASE.value,
        required=True,
    )

    download_url = fields.Char("Download URL", compute="_compute_download_url", store=False)
    is_disk = fields.Boolean(compute="_compute_is_disk", store=False)
    is_saved = fields.Boolean(compute="_compute_is_saved", store=False)

    @api.depends("storage_type", "file_path")
    def _compute_download_url(self) -> None:
        for record in self:
            record.download_url = self._build_file_download_url(record) if self._is_disk_stored(record) and record.file_path else ""

    @api.depends("storage_type")
    def _compute_is_disk(self) -> None:
        for record in self:
            record.is_disk = self._is_disk_stored(record)

    def _compute_is_saved(self) -> None:
        for record in self:
            record.is_saved = bool(record.id)

    @api.model
    def create(self, vals: dict) -> 'FileManager':
        record = super().create(vals)

        if vals.get("storage_type") == StorageType.DISK.value:
            record.move_file_to_disk()

        return record

    def unlink(self) -> None:
        """Overrides unlink to handle file deletion from disk storage."""

        for record in self:
            if self._is_disk_stored(record) and record.file_path:
                try:
                    os.remove(record.file_path)

                except Exception as e:
                    raise UserError(f"Failed to remove file from disk: {e}")

        return super().unlink()

    def move_file_to_disk(self) -> None:
        """Moves the uploaded file from database storage to disk storage."""

        self.ensure_one()
        if not self._is_disk_stored(self) or not self.file_data:
            return

        file_content = base64.b64decode(self.file_data)
        file_path = os.path.join(self.__get_file_storage_dir(), self.name)

        try:
            with open(file_path, "wb") as file:
                file.write(file_content)

            self.write({"file_path": file_path, "file_data": False})

        except Exception as e:
            raise UserError(f"Failed to save file on disk: {e}")

    @staticmethod
    def __get_file_storage_dir() -> Optional[str]:
        """Retrieves the file storage directory from system parameters."""

        storage_dir = tools.config.get('storage_dir')
        os.makedirs(storage_dir, exist_ok=True)

        return storage_dir

    def _build_file_download_url(self, record: 'FileManager') -> str:
        """Constructs the URL to download the file."""

        return f"{self._web_base_url}/files/download/{record.id}"

    @staticmethod
    def _is_disk_stored(record: 'FileManager') -> bool:
        """Determines if the file is stored on disk."""

        return record.storage_type == StorageType.DISK.value

    @cached_property
    def _web_base_url(self) -> str:
        """Retrieves the base web URL from system parameters."""

        return self.env["ir.config_parameter"].sudo().get_param("web.base.url")

