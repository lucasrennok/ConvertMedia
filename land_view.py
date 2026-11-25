import os
import shutil
import subprocess

import FreeSimpleGUI as sg
from PIL import Image

# Extensões que tratamos como imagem (convertidas com Pillow).
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp"}


def ffmpeg_available() -> bool:
    """Verifica se o ffmpeg está instalado e no PATH."""
    return shutil.which("ffmpeg") is not None


def convert_image(src: str, dst: str) -> None:
    with Image.open(src) as img:
        # JPEG não tem canal alfa; converte para RGB antes de salvar.
        if dst.lower().endswith((".jpg", ".jpeg")) and img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(dst)


def convert_with_ffmpeg(src: str, dst: str) -> None:
    # Lista de argumentos (sem shell) evita problemas com espaços no nome.
    subprocess.run(
        ["ffmpeg", "-y", "-i", src, dst],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


class LandScreen:
    def __init__(self) -> None:
        layout = [
            [
                sg.Text("Converter:"),
                sg.Radio("Imagem", "media", key="image", default=True),
                sg.Radio("Vídeo / Áudio", "media", key="video"),
            ],
            [sg.Text("Arquivo de entrada", size=(16, 1)), sg.Input(key="filename"), sg.FileBrowse("Procurar")],
            [sg.Text("Arquivo de saída", size=(16, 1)), sg.Input(key="newFilename"), sg.Text("(ex.: saida.mp3)")],
            [sg.Button("Converter", key="convert"), sg.Button("Sair", key="quit")],
            [sg.Text("", key="status", size=(50, 1), text_color="yellow")],
        ]
        self.window = sg.Window("ConvertMedia", layout)

    def convert(self) -> str:
        event, data = self.window.read()

        if event in (sg.WIN_CLOSED, "quit"):
            return "quit"

        if event == "convert":
            src = (data["filename"] or "").strip()
            dst = (data["newFilename"] or "").strip()

            if not src or not dst:
                self._status("Preencha os dois nomes de arquivo.")
                return "convert"
            if not os.path.isfile(src):
                self._status(f"Arquivo não encontrado: {src}")
                return "convert"

            try:
                if data["image"]:
                    convert_image(src, dst)
                else:
                    if not ffmpeg_available():
                        self._status("FFmpeg não encontrado no PATH. Veja o README.")
                        return "convert"
                    convert_with_ffmpeg(src, dst)
                self._status(f"Pronto! Gerado: {dst}")
            except subprocess.CalledProcessError:
                self._status("Falha na conversão com FFmpeg (formato inválido?).")
            except Exception as err:  # noqa: BLE001 — mostra o erro na interface
                self._status(f"Erro: {err}")

        return "convert"

    def _status(self, message: str) -> None:
        self.window["status"].update(message)

    def closeWindow(self) -> None:
        self.window.close()
