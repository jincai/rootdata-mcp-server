# RootData MCP Server

这是一个基于 [Model Context Protocol (MCP)](https://github.com/microsoft/model-context-protocol) 的服务器，用于集成 RootData API，提供加密货币和区块链项目的数据查询功能。

## 功能特点

本服务器实现了 RootData API 的以下功能：

1. **搜索项目/VC/人物** - 根据关键词搜索项目、风投机构或人物的简要信息
2. **获取项目详情** - 根据项目 ID 获取项目的详细信息
3. **获取 VC 详情** - 根据机构 ID 获取风投机构的详细信息

## 安装与配置

### 前提条件

- Python 3.8 或更高版本
- RootData API 密钥（需要在 [RootData](https://www.rootdata.com/) 申请）

### 安装步骤

1. 克隆仓库：

```bash
git clone https://github.com/jincai/rootdata-mcp-server.git
cd rootdata-mcp-server
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：

```bash
cp .env.example .env
```

然后编辑 `.env` 文件，填入你的 RootData API 密钥：

```
ROOTDATA_API_KEY=your_api_key_here
```

### 启动服务器

```bash
python server.py
```

服务器默认在 `http://localhost:8000` 启动。

## MCP 工具说明

本服务器提供以下 MCP 工具：

### 1. search

搜索项目/VC/人物的简要信息。

**参数：**
- `query` (string, 必填): 搜索关键词，可以是项目/机构名称、代币符号等。

**示例：**
```json
{
  "query": "Ethereum"
}
```

### 2. get_project

获取项目的详细信息。

**参数：**
- `project_id` (integer, 必填): 项目的唯一标识符。
- `include_team` (boolean, 可选): 是否包含团队成员信息，默认为 false。
- `include_investors` (boolean, 可选): 是否包含投资者信息，默认为 false。

**示例：**
```json
{
  "project_id": 12,
  "include_team": true,
  "include_investors": true
}
```

### 3. get_organization

获取风投机构的详细信息。

**参数：**
- `org_id` (integer, 必填): 机构的唯一标识符。
- `include_team` (boolean, 可选): 是否包含团队成员信息，默认为 false。
- `include_investments` (boolean, 可选): 是否包含投资项目信息，默认为 false。

**示例：**
```json
{
  "org_id": 219,
  "include_team": true,
  "include_investments": true
}
```

## 与 LLM 集成

要将此 MCP 服务器与支持 MCP 的大型语言模型（如 Claude 3）集成，请确保：

1. 服务器正在运行并可访问
2. 在 LLM 会话中注册此 MCP 服务器
3. 使用 LLM 的 MCP 工具调用功能来访问 RootData 数据

## 许可证

MIT
