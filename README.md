# ine5420

Para rodar o trabalho use o seguinte comando:
```bash
make run
```

É necessário que o tkinter esteja instalado e que a versão do python maior ou igual à 3.10


## Salvar e carregar objetos
Para carregar objetos de arquivos .obj, é necessário que tal arquivo siga
o seguinte formato:
```plaintext
o point1
usemtl red
v 33 130 1
p -1

o line1
usemtl blue
v 200 100 1
v 150 200 1
l -1 -2

o triangle1
usemtl yellow
v 100 300 1
v 300 300 1
v 200 400 1
f -1 -2 -3
```

OBS: apenas índices relativos são suportados.