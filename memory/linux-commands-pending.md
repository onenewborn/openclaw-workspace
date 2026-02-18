# Linux 命令学习记录 (待同步到 Google Sheets)

## 2026-02-14

### 1. 系统配置 - 添加 PATH 环境变量
```bash
echo 'export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:$PATH"' >> ~/.zshrc
```

**拆解**:
1. `echo` — 输出文本内容
2. `export PATH...` — 要写入的环境变量声明，将 Python 3.12 路径加入系统 PATH
3. `>>` — 追加运算符，将内容添加到文件末尾而不覆盖
4. `~/.zshrc` — zsh shell 的配置文件，终端启动时自动执行

**用途**: 配置 Homebrew 安装的 Python 3.12 路径，让系统能找到它

---

### 2. 网络操作 - curl 安装脚本
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**拆解**:
1. `curl` — 命令行 HTTP 客户端，用于下载文件
2. `-L` — 跟随重定向（如果链接被跳转，自动跟随）
3. `-s` — 静默模式（不显示下载进度）
4. `-S` — 出错时显示错误信息（和 -s 搭配使用）
5. `-f` — 失败时不输出内容（HTTP 错误码时静默）
6. `URL` — 要下载的 uv 安装脚本地址
7. `| sh` — 管道传给 shell 执行，实现在线安装

**用途**: 安装 `uv` — 用 Rust 写的超快 Python 包管理器（比 pip 快 10-100 倍）

**注意**: 这种 `curl ... | sh` 的安装方式很方便，但要确保来源可信（astral.sh 是 uv 官方地址）
