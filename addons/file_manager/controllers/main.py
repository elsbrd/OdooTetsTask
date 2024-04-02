import os

from odoo import http
from odoo.http import request, Response
from odoo.addons.file_manager.models.file_manager import FileManager


class FileDownloadController(http.Controller):
    @http.route(
        '/files/download/<model("file.manager"):file_record>', auth="user", type="http"
    )
    def download_file(self, file_record: FileManager, **kwargs) -> Response:
        if (
            file_record.storage_type == "disk"
            and file_record.file_path
            and os.path.exists(file_record.file_path)
        ):
            return self._serve_disk_file(file_record)

        return request.not_found()

    def _serve_disk_file(self, file_record: FileManager) -> Response:
        with open(file_record.file_path, "rb") as file:
            file_content = file.read()

        headers = self.__prepare_headers(file_record)

        return request.make_response(file_content, headers)

    @staticmethod
    def __prepare_headers(file_record: FileManager):
        return [
            ("Content-Type", "application/octet-stream"),
            ("Content-Disposition", f'attachment; filename="{file_record.name}"'),
        ]
