import platform

if platform.system() == "Windows":
    caminho = "C:/Users/richa/Desktop/cursos/comerga/credenciais"
else:
    caminho = "/home/richardmbs_rs/comerga/credenciais"

AWS_ACCESS_KEY_ID = open(caminho + "/AWS_ACCESS_KEY_ID.txt", encoding="utf8").read()

AWS_SECRET_ACCESS_KEY =  open(caminho + "/AWS_SECRET_ACCESS_KEY.txt", encoding="utf8").read()

DB =  open(caminho + "/PASSWORD-DB.txt", encoding="utf8").read()

KEY_API_GOOGLE =  open(caminho + "/KEY_API_GOOGLE.txt", encoding="utf8").read()