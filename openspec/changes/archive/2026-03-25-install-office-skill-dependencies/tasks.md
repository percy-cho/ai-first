## 1. 安装 Python 依赖

- [x] 1.1 安装 pypdf (PDF 基础操作)
- [x] 1.2 安装 pdfplumber (PDF 文本/表格提取)
- [x] 1.3 安装 reportlab (创建 PDF)
- [x] 1.4 安装 pdf2image (PDF 转图像)
- [x] 1.5 安装 pytesseract (OCR 扫描 PDF)
- [x] 1.6 安装 openpyxl (Excel 公式/格式化)
- [x] 1.7 安装 pandas (数据分析)
- [x] 1.8 安装 markitdown[pptx] (PPTX 文本提取)
- [x] 1.9 安装 Pillow (图像处理)

**安装命令**:
```bash
pip install --break-system-packages pypdf pdfplumber reportlab pdf2image pytesseract openpyxl pandas markitdown[pptx] Pillow
```

## 2. 安装 Node.js 依赖

- [x] 2.1 安装 docx (Word 文档生成)
- [x] 2.2 安装 pptxgenjs (PowerPoint 生成)

**安装命令**:
```bash
npm install -g docx pptxgenjs
```

## 3. 安装系统工具

- [x] 3.1 安装 pandoc (文档转换)
- [x] 3.2 安装 LibreOffice (文档处理)
- [x] 3.3 安装 poppler-utils (pdftoppm)
- [x] 3.4 安装 qpdf (PDF 命令行操作)
- [x] 3.5 安装 pdftk (PDF 工具)
- [x] 3.6 安装 tesseract-ocr (OCR 引擎)

**安装命令**:
```bash
sudo apt install -y pandoc libreoffice poppler-utils qpdf pdftk tesseract-ocr
```

## 4. 验证安装

- [x] 4.1 验证 Python 包可导入
- [x] 4.2 验证 Node.js 包已全局安装
- [x] 4.3 验证系统工具可用
- [x] 4.4 检查所有依赖版本

**验证命令**:
```bash
# Python 包
python3 -c "import pypdf, pdfplumber, reportlab, pdf2image, pytesseract, openpyxl, pandas, markitdown, PIL; print('OK')"

# Node.js 包
npm list -g docx pptxgenjs

# 系统工具
which pandoc libreoffice pdftoppm qpdf pdftk tesseract
```
