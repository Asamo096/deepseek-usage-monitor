# DeepSeek API 用量监控

> Forked from [Shiorangerin/deepseek-usage-monitor](https://github.com/Shiorangerin/deepseek-usage-monitor)

一个复古像素风桌面小组件，实时监控你的 DeepSeek API 用量。数据来自 [platform.deepseek.com](https://platform.deepseek.com/usage) 内部接口。

## 功能

- **余额看板** — 剩余余额及彩色进度条（<15% 红色、<40% 琥珀色、>40% 蓝色）
- **每日 Token 统计** — 总计、输入、输出 token 及迷你条形图
- **缓存命中率** — 醒目显示及颜色阈值（>80% 绿色、>50% 蓝色、<50% 橙色）
- **费用追踪** — 今日花费与月度花费（¥，精确到 4 位小数）
- **柱状图上限可调** — 在 `config.json` 中设置 Token/Cost 柱状图最大显示值，超出部分自动截断，方便对比差距悬殊的数据（Cost 值以人民币为单位，切换币种自动换算）
- **赠额显示** — 单独展示免费额度
- **可配置刷新** — 在 `config.json` 中设置刷新间隔（默认 10 秒，最少 3 秒）
- **悬停虚化** — 鼠标悬停时淡出至 25% 透明度，移开恢复（可在系统托盘切换）
- **系统托盘** — 最小化到托盘，支持显示/隐藏、虚化开关、刷新和退出
- **置顶显示** — 始终位于所有窗口之上
- **拖拽移动** — 左键按住任意位置拖拽
- **滚动语录** — 底部轮播 60+ 条 AI 笑话
- **像素风界面** — 深色主题、Courier New 等宽字体、高对比度布局
- **通知栏显示** — 数据更新时通过系统通知栏提醒（可开关）
- **充值入口** — 右键菜单快速跳转充值页面

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如需系统托盘功能（推荐）：

```bash
pip install pystray pillow
```

### 2. 获取 Token

1. 使用 **Chrome** 浏览器打开 [platform.deepseek.com](https://platform.deepseek.com/usage) 并登录
2. 按 **F12** → **控制台**，粘贴以下代码：

```js
JSON.parse(localStorage.getItem('userToken')).value
```

3. 复制输出的字符串

### 3. 运行

```bash
双击 main.pyw
```

首次启动会弹出对话框要求粘贴 token，随后自动保存到 `config.json`。

## 配置文件 (`config.json`)

| 键名 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `bearer_token` | string | — | 平台认证令牌 |
| `refresh_interval` | integer | 10 | 自动刷新间隔（秒，最少 3 秒） |
| `hover_fade` | boolean | true | 鼠标悬停时虚化 |
| `chart_max_display` | object | — | 柱状图最大显示值，详见下方说明 |
| `notify_on_update` | boolean | false | 数据更新时通知栏显示 |

`chart_max_display` 格式示例：

```json
"chart_max_display": {
  "token": 5000000,
  "cost": 5
}
```

- `token` — Token 柱状图最大显示值（单位：tokens），超过此值的柱子以最高高度显示
- `cost` — 费用柱状图最大显示值（单位：**人民币**），超过此值的柱子以最高高度显示；切换为其他币种（USD/CAD/JPY）时自动按汇率换算
- 不设置或设为 `null` 时自动根据数据最大值适配（原行为）

> 注意：此设置仅影响柱状图的**视觉显示高度**，不改变数据的实际数值和准确性。鼠标悬停时 tooltip 内仍显示真实值。

## 操作方式

| 操作 | 效果 |
|------|------|
| 左键拖拽 | 移动窗口 |
| 右键 | 右键菜单（刷新 / 图表 / 热力图 / 模式切换 / 充值 / 退出等） |
| 托盘左键 | 切换显示/隐藏 |
| 托盘右键 | 右键菜单 |
| 鼠标悬停 | 淡出至 25% 透明度 |

## 项目结构

```
deepseek-usage-monitor/
├── main.pyw             # 入口 + 系统托盘
├── widget.py            # 像素风界面
├── api.py               # 内部 API 客户端
├── config.py            # 配置管理器
├── token_extractor.py   # 可选的 Chrome 自动提取
├── heatmap.py           # 热力图数据管理
├── config.json          # Token 与设置（已加入 gitignore）
├── requirements.txt     # Python 依赖
├── LICENSE              # CC BY-NC 4.0 许可证
├── README.md
└── .gitignore
```

## 注意事项

- Token 有效期为数天至数周。如果数据停止更新，删除 `config.json` 重新运行即可。
- 内部 API 并非官方文档接口，platform.deepseek.com 变更后可能失效。
- Playwright 自动提取 Token 为可选功能：`pip install playwright && playwright install chromium`

## 许可证

本项目采用 [CC BY-NC 4.0](LICENSE)（署名-非商业性使用 4.0 国际许可协议）。

你可以自由地：
- **共享** — 在任何媒介以任何形式复制、发行本作品
- **演绎** — 修改、转换或以本作品为基础进行创作

惟须遵守下列条件：
- **署名** — 你必须给出适当的署名。
- **非商业性使用** — 你不得将本作品用于商业目的。

完整许可证文本：https://creativecommons.org/licenses/by-nc/4.0/legalcode
