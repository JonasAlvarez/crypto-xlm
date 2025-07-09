# crypto-xlm
## Storing the XLM in paper

The generation process:
1. pull the image with:
    ```bash
    docker pull python:3.11-slim-bookworm
    ```
3. create the keys, it will ask for a password or secret:
   ```bash
   chmod +x secure_xlm_wallet.sh
   ./secure_xlm_wallet.sh
   ```
5. paste the QR and associated info in notepad (font console 9) and print

The result in the pdf.



For using the keys, paste here the encrypted private key:
```bash
python decrypt_xlm_key.py
```
