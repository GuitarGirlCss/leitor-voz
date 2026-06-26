# 📢 Leitor de Texto em Voz Alta

Lê qualquer texto em voz alta com interface simples e acessível. Ideal para escolas e alunos com dificuldades de leitura. Funciona também como monitor automático, basta copiar um texto em qualquer site para ouvi-lo instantaneamente.

## ✅ Requisitos

- Python 3
- Bibliotecas: `pyttsx3` e `pyperclip`

## 📦 Instalação

```bash
pip install pyttsx3 pyperclip
```

## ▶️ Como usar

### Modo manual
1. Execute o script:
   ```bash
   python leitor.py
   ```
2. Cole ou digite o texto na caixa
3. Escolha o idioma e ajuste a velocidade
4. Clique em **Ouvir texto**

### Modo monitor (sites)
1. Clique em **"Ativar monitor de cópia"**
2. Vá para qualquer site no navegador
3. Selecione o texto desejado e pressione **Ctrl+C**
4. O programa detecta automaticamente e lê em voz alta

## ⚙️ Funcionalidades

- 🔊 Leitura em voz alta de qualquer texto
- 🌐 Seleção de idioma (Português, Inglês, Espanhol, Francês, Alemão, Italiano)
- 🐢🐇 Controle de velocidade da fala
- ⏹ Botão para parar a leitura a qualquer momento
- 🗑 Botão para limpar o texto
- 📋 Monitor automático de área de transferência
- 💻 Funciona 100% offline

## 🖥️ Vozes suportadas

O programa usa as vozes instaladas no seu sistema. No Windows, as vozes padrão são:
- **Microsoft Maria** — Português (Brasil)
- **Microsoft Zira** — Inglês (EUA)

Para mais idiomas, instale vozes adicionais em: `Configurações → Hora e idioma → Fala`
