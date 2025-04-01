from fastapi import FastAPI, UploadFile, File
import boto3
import os

app = FastAPI()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
)

BUCKET_NAME = os.environ.get("BUCKET_NAME")

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de FastAPI con App Runner y S3"}

@app.post("/subir-archivo")
def subir_archivo(archivo: UploadFile = File(...)):
    s3.upload_fileobj(archivo.file, BUCKET_NAME, archivo.filename)
    return {"mensaje": f"Archivo '{archivo.filename}' subido correctamente a S3"}

@app.get("/listar-archivos")
def listar_archivos():
    objetos = s3.list_objects_v2(Bucket=BUCKET_NAME)
    archivos = [obj['Key'] for obj in objetos.get('Contents', [])]
    return {"archivos": archivos}
