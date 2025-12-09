
```markdown
# BuggyPaperTranslator
学术论文摘要翻译工具：自动将英文论文摘要批量翻译成中文，支持断点续传、进度显示，适配Hugging Face最新接口。


## 功能说明
- 批量翻译：读取CSV格式的论文列表，自动翻译`abstract`列的英文摘要；
- 断点续传：程序中断后，重新运行可跳过已翻译内容；
- 进度可视化：通过`tqdm`显示翻译进度；
- 稳定可靠：内置重试机制，应对网络波动/接口限流。


## 环境配置
### 1. 克隆仓库
```bash
git clone https://github.com/Jimmy980212/task0.git
cd task0
```

### 2. 安装依赖
使用修复后的依赖文件：
```bash
pip install -r requirements.txt
```

### 3. 配置Token
在项目根目录创建`.env`文件，填入你的Hugging Face Token：
```env
HF_TOKEN=你的Hugging Face Access Token（需具备Read权限）
```


## 运行步骤
1. 准备输入文件：确保`iccv2025.csv`存在于项目根目录（需包含`abstract`列）；
2. 启动翻译：
```bash
python translator_legacy.py
```
3. 查看结果：翻译完成后，结果会保存到`result.csv`（包含`row_num`和`cn_abstract`列）。


## 注意事项
- Token获取：在[Hugging Face Settings](https://huggingface.co/settings/tokens)创建`Read`权限的Token；
- 接口限制：Hugging Face接口存在限流，若遇429错误，程序会自动重试；
- 断点续传：`result.csv`会记录已翻译内容，请勿手动删除该文件。
```

