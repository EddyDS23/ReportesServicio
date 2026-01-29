# Build de ejecutable (.exe) en Windows

Este README describe **únicamente** el proceso para:

* crear un entorno virtual (`venv`)
* instalar dependencias con `pip` usando `requirements.txt`
* compilar la aplicación en un `.exe`

Proyecto basado en **PySide6** y **ReportLab**.

---

## 📁 Estructura del proyecto

```text
proyecto/
│── main.py
│── requirements.txt
│
├── models/
│   ├── report.py
│   └── activities.py
│
├── ui/
│   ├── main_window.py
│   ├── activity_dialog.py
│   └── styles.py
│
└── services/
    └── pdf_generator.py
```

---

## 1️⃣ Crear entorno virtual (venv)

Desde la raíz del proyecto:

```powershell
python -m venv venv
```

Activar el entorno virtual:

```powershell
venv\Scripts\activate
```

La terminal debe mostrar:

```text
(venv)
```

---

## 2️⃣ Instalar dependencias

Actualizar `pip` e instalar dependencias desde `requirements.txt`:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Ejemplo de `requirements.txt`:

```text
PySide6
reportlab
```

Probar la aplicación antes de compilar:

```powershell
python main.py
```

---

## 3️⃣ Instalar PyInstaller

Dentro del entorno virtual:

```powershell
pip install pyinstaller
```

---

## 4️⃣ Compilar el ejecutable (.exe)

Ejecutar PyInstaller desde la raíz del proyecto:

```powershell
pyinstaller --onefile --windowed main.py
```

El ejecutable se generará en:

```text
dist/main.exe
```

---

## 5️⃣ Resultado

El archivo `main.exe`:

* incluye Python y todas las dependencias
* no requiere Python instalado en la máquina final
* puede ejecutarse directamente en Windows
