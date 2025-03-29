# RootData MCP Server

## Introduction

这是一个基于 [Model Context Protocol (MCP)](https://github.com/microsoft/model-context-protocol) 的服务器，用于集成 RootData API，提供加密货币和区块链项目的数据查询功能。

它允许 Claude 和其他 AI 助手通过 MCP 接口直接获取项目信息、机构详情和搜索结果。

## Available Tools

本服务器提供以下 MCP 工具：

* **search**: 根据关键词搜索项目/VC/人物的简要信息
* **get_project**: 根据项目 ID 获取项目的详细信息
* **get_organization**: 根据机构 ID 获取风投机构的详细信息

## Setup

### Prerequisites

* Python 3.10 或更高版本
* [uv](https://github.com/astral-sh/uv) 包管理器（推荐）

### Installation

1. 克隆此仓库：

```shell
git clone https://github.com/jincai/rootdata-mcp-server
cd rootdata-mcp-server
```

2. 如果你还没有安装 uv，可以安装它：

```shell
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
curl -LsSf https://astral.sh/uv/install.ps1 | powershell
```

3. 安装依赖：

```shell
# 创建虚拟环境并激活
uv venv
source .venv/bin/activate  # Windows 上: .venv\Scripts\activate

# 安装依赖
uv add "mcp[cli]" httpx python-dotenv
```

4. 设置环境变量：

```shell
# 创建 .env 文件存储 API 密钥
cp .env.example .env

# 在 .env 文件中设置 API 密钥
ROOTDATA_API_KEY=your-rootdata-api-key
```

5. 运行服务器：

```shell
uv run server.py
```

## Connecting to Claude Desktop

1. 安装 [Claude Desktop](https://claude.ai/desktop)（如果你还没有安装）

2. 创建或编辑 Claude Desktop 配置文件：

```shell
# macOS
mkdir -p ~/Library/Application\ Support/Claude/
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

3. 添加以下配置：

```json
{
  "mcpServers": {
    "rootdata": {
      "command": "/path/to/uv",
      "args": [
        "--directory",
        "/absolute/path/to/rootdata-mcp-server",
        "run",
        "server.py"
      ]
    }
  }
}
```

将 `/path/to/uv` 替换为 `which uv` 的结果，将 `/absolute/path/to/rootdata-mcp-server` 替换为此项目的绝对路径。

4. 重启 Claude Desktop

5. 现在你应该能在 Claude Desktop 的工具菜单（锤子图标）中看到 RootData 工具

6. 尝试向 Claude 提问，例如：
   * "搜索以太坊相关的项目"
   * "获取项目 ID 为 12 的详细信息"
   * "查询机构 ID 为 219 的风投机构信息"

## License

MIT
