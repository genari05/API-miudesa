from flask_restx import Api

api = Api(
    version="1.0",
    title="𝚿 API MIUDESA 𝚿",
    description="Documentação da API sobre clinica psicoterapia ",
    doc="/",
    mask_swagger=False,
)