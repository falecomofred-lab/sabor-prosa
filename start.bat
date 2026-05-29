@echo off
title Sabor e Prosa Emporio - Sistema de Gestao
color 0E
echo ========================================
echo   ???  SABOR E PROSA EMPORIO
echo   Iniciando o sistema...
echo ========================================
echo.
echo ?? Verificando dependencias...
pip install -r requirements.txt --quiet
echo.
echo ???  Preparando banco de dados...
if exist sabor_prosa.db (
    echo    Banco existente: OK
) else (
    echo    Criando novo banco...
)
echo.
echo ?? Iniciando servidor...
echo.
echo ========================================
echo   ? Sistema rodando!
echo   ?? Acesse: http://localhost:8000/dashboard
echo   ?? PDV: http://localhost:8000/pdv
echo   ?? Produtos: http://localhost:8000/produtos
echo   ?? Chat IA disponivel no botao flutuante
echo ========================================
echo.
echo   Pressione CTRL+C para parar o servidor
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
pause
