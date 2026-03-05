@echo off

echo ================================
echo MCP Data Query Builder Demo
echo ================================
echo.

echo Choose prompting strategy:
echo 1 - Minimal
echo 2 - Structured
echo 3 - Expert Workflow
echo.

set /p choice=Enter choice (1-3): 

if "%choice%"=="1" (
    copy prompts\minimal.md GEMINI.md >nul
    echo Minimal prompt selected.
)

if "%choice%"=="2" (
    copy prompts\structured.md GEMINI.md >nul
    echo Structured prompt selected.
)

if "%choice%"=="3" (
    copy prompts\expert.md GEMINI.md >nul
    echo Expert workflow prompt selected.
)

echo.
echo Starting MCP server...

start "" /B mcp run server.py

timeout /t 2 >nul

echo.
echo Starting Gemini CLI...
gemini