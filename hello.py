#!/usr/bin/python3
hello="""
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <title>Enviar Texto</title>
    <style>
        body {
            background-color: yellow;
            font-family: Arial, sans-serif;
        }
            </style>
</head>
<body>
    hello world....
</body>
</html>
"""
print("Content-type:text-html\r\n\r\n\n")
print(hello)