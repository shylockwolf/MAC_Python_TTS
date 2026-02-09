# MAC Python TTS

一个基于 Python 的文本转语音 (TTS) 项目，支持中英文语音合成。

## 项目结构

```
MAC_Python_TTS/
├── models/           # 语音模型目录
├── __pycache__/      # Python 缓存目录
├── download_model.py # 模型下载脚本
├── tts_app.py        # 主应用脚本
├── test_input.txt    # 测试输入文件
├── test01.wav        # 测试输出文件
├── test02.wav        # 测试输出文件
└── .gitignore        # Git 忽略文件
```

## 功能特性

- 支持中英文文本转语音
- 使用预训练的 ONNX 模型
- 简单易用的命令行接口

## 依赖安装

1. 确保已安装 Python 3.8 或更高版本
2. 安装所需依赖：

```bash
pip install numpy onnxruntime sounddevice soundfile requests python-dotenv
```

## 模型下载

运行模型下载脚本获取所需的语音模型：

```bash
python download_model.py
```

## 使用方法

### 图形界面使用

1. 运行应用程序：

```bash
python tts_app.py
```

2. 在界面中选择 TTS 模式：
   - **Local Model**：使用本地安装的模型
   - **NVIDIA Magpie API**：使用 NVIDIA 的云端 TTS API

3. 根据选择的模式进行配置：
   - **Local Model**：从下拉菜单中选择本地语音模型
   - **NVIDIA Magpie API**：从下拉菜单中选择 API 语音模型

4. 点击 "Browse..." 按钮选择包含文本的 .txt 文件

5. 点击 "Generate Audio" 按钮生成音频文件

### NVIDIA Magpie API 配置

1. 从 [NVIDIA Build](https://build.nvidia.com/nvidia/magpie-tts-multilingual) 获取 API 密钥

2. 编辑 `.env` 文件，添加你的 API 密钥：

```env
NVIDIA_API_KEY=your_api_key_here
```

3. 保存文件并重新运行应用程序

## 支持的模型

- `zh_CN-huayan-medium.onnx` - 中文女声模型
- `en_US-amy-medium.onnx` - 英文女声模型

## 注意事项

- 生成的 WAV 文件和 models 目录已添加到 .gitignore 文件中，不会被 Git 追踪
- 首次运行需要下载模型文件，可能需要一些时间
- 确保有足够的磁盘空间存储模型文件

## 许可证

MIT License
