>[!IMPORTANT]
>Projeto em desenvolvimento versão Alpha 1.0.

# Como iniciar a API Konexo

## Passo 1: Clone e acesse o repositório localmente

```bash
git clone https://github.com/KonexoGS/api-konexo
cd api-konexo
```

## Passo 2: Inicie um ambiente virtual e instale as dependências

### Criando e iniciando o ambiente virtual

```bash
python -m venv .venv # Cria um novo ambiente virtual
```

### Iniciando o ambiente virtual

Os comandos abaixo correspondem ao seu OS ativo na máquina, escolha somente **um** deles.:

```bash
# Linux, macOs
source .venv/bin/activate

# Windows
.venv\Scripts\Activate.ps1 # powershell
source .venv/Scripts/activate # Win bash
```

### Verifique o ambiente

```bash
# Linux, macOS
which python

# Windows Powershell
Get-Command python
```

## Passo 3: Instale as depêndencias em [requirements.txt](https://github.com/KonexoGS/api-konexo/blob/main/requirements.txt)

O comando abaixo irá atualizar o pip para a última versão e instalar as dependências da api

```bash
pip install --upgrade pip && pip install -r requirements.txt 
```

## Passo 4: Iniciar a API Konexo

```bash
cd app
fastapi run main.py # Inicia a API
```

---

**Prontinho!**, agora você consegue testar a api como quiser. Para testar as rotas no Swagger acesse **/docs** ao iniciar a API.
