# FocusEd

**Title / Título:** FocusEd  
**Author / Autor:** Paul Regnier

---

### 📄 Description / Descrição

**EN:**  
Allows users to create, manage, and download lesson observations

**BR:**  
Permite aos usuários criar, gerenciar e baixar observações de aula

---

### ✨ Features / Características

**EN:**
- Intuitive forms for creating new observations
- Dynamic tables for viewing and managing observations
- Downloading observations as PDFs

**BR:**
- Formulários intuitivos para criar novas observações
- Tabelas dinâmicas para visualizar e gerenciar observações
- Download de observações em formato PDF

---

### 🛠 Tech Stack / Tecnologias

- **Language / Linguagem:** Python 3.11.2  
- **Framework:** FastAPI  
- **Database / Banco de dados:** SQLite, SQLAlchemy  
- **Data validation / Validação de dados:** Pydantic, SQLAlchemy  
- **PDF Generation / Geração de PDF:** WeasyPrint  
- **Dependency Management / Gerenciamento de dependências:** `venv`, `requirements.txt`

---

### ✅ Prerequisites / Pré-requisitos

**EN:**
- Python 3.11 or higher
- Web browser
- Command line access
- Backend must be run from the `backend/` directory

**BR:**
- Python 3.11 ou superior
- Navegador web
- Acesso ao terminal ou prompt de comando
- O backend deve ser executado a partir do diretório `backend/`

---

### 🧪 Installation & Launch / Instalação e Execução

**EN:**
# Clone the repository / Clone o repositorio
git clone https://github.com/reg75/focused.git
cd focused/backend

# Create and activate a virtual environment / Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies / Instale as dependencias
pip install -r requirements.txt

# Run the FastAPI server / Execute o servidor FastAPI
uvicorn app.main:app --reload
