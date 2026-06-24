#!/bin/bash
PROJ_ROOT="$(realpath "$(dirname "${0}")/../../")"
FILE="secret.enc"

source "${PROJ_ROOT}/.venv/bin/activate"
python "${PROJ_ROOT}/src/cryptographics/crypt.py" decrypt "${PROJ_ROOT}/wiki/${FILE}" "${PROJECT_ROOT}wiki/whatsapp_chat_decrypted.txt"
