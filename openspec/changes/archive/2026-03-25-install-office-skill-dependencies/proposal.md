## Why

.agents/skills 目录下的四个 Office 相关 skill（docx、pdf、pptx、xlsx）需要依赖外部工具才能正常工作。这些依赖包括 Python 库、Node.js 包和系统工具。缺少这些依赖会导致 skill 无法执行文档创建、编辑和分析等操作。

## What Changes

安装以下依赖：

### Python 包
- **pypdf** - PDF 基础操作（合并/拆分/旋转）
- **pdfplumber** - PDF 文本和表格提取
- **reportlab** - 创建 PDF 文档
- **pdf2image** - PDF 转图像
- **pytesseract** - OCR 扫描 PDF 文字识别
- **openpyxl** - Excel 公式和格式化
- **pandas** - 数据分析和处理
- **markitdown[pptx]** - PPTX 文本提取
- **Pillow** - 图像处理

### Node.js 包
- **docx** (docx-js) - Word 文档生成
- **pptxgenjs** - PowerPoint 幻灯片生成

### 系统工具
- **pandoc** - 文档格式转换
- **LibreOffice** - 文档处理和公式计算
- **pdftoppm** (Poppler) - PDF 转图像
- **qpdf** - PDF 命令行操作
- **pdftk** - PDF 合并/拆分工具
- **tesseract** - OCR 引擎

## Capabilities

### New Capabilities
<!-- 无新 capability，此 change 仅为环境准备 -->

### Modified Capabilities
<!-- 无现有 capability 修改 -->

## Impact

- **系统环境**: 安装系统级软件包（需要 sudo 权限）
- **Python 环境**: 全局安装 Python 包（使用 --break-system-packages）
- **Node.js 环境**: 全局安装 npm 包
- **磁盘空间**: 约 500MB-1GB（主要来自 LibreOffice 和 Python 包）
- **现有项目**: 无影响，仅添加依赖不修改代码
