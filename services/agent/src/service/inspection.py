from uuid import uuid4
from src.api.schemas import InspectionReport

MAX_BYTES = 10 * 1024 * 1024
SIGNATURES = {
    "image/jpeg": lambda data: data.startswith(b"\xff\xd8\xff"),
    "image/png": lambda data: data.startswith(b"\x89PNG\r\n\x1a\n"),
    "image/webp": lambda data: data.startswith(b"RIFF") and data[8:12] == b"WEBP",
}


def inspect_image(content: bytes, content_type: str | None) -> InspectionReport:
    if not content:
        raise ValueError("Arquivo vazio.")
    if len(content) > MAX_BYTES:
        raise ValueError("Imagem excede limite configurado.")
    if content_type not in SIGNATURES or not SIGNATURES[content_type](content):
        raise ValueError("Conteúdo não corresponde a formato JPEG, PNG ou WEBP.")
    return InspectionReport(
        inspection_id=str(uuid4()),
        summary="Imagem recebida. Análise visual automatizada ainda não disponível.",
        observations=["Nenhum componente foi identificado automaticamente nesta versão."],
        required_information=[
            "Tensão nominal e número de fases do circuito",
            "Seção, material e método de instalação dos condutores",
            "Dispositivo de proteção e características da carga",
            "Verificação presencial por profissional habilitado",
        ],
        limitations=[
            "Fotografias isoladas não comprovam conformidade com normas técnicas.",
            "Não altere disjuntores, tomadas ou fiação com base neste relatório.",
        ],
    )
