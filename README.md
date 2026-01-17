# 可转债申购自动提醒系统

这是一个能在GitHub Actions上自动运行的可转债申购提醒工具，每天定时扫描当天是否有可申购的新债，并通过多种方式通知你。

## 🎯 功能特点

- 🔄 **自动扫描**：每个工作日早上8点自动运行
- 📊 **多数据源**：使用东方财富网数据源，确保信息准确
- 🔔 **多渠道通知**：支持邮件、钉钉、企业微信、Server酱等多种通知方式
- 🚀 **零成本部署**：利用GitHub Actions免费额度，无需服务器
- 📱 **即时提醒**：有新股申购时立即推送通知

## 📁 项目结构

```
├── .github/workflows/
│   └── check_bonds.yml      # GitHub Actions工作流配置
├── check_new_bonds.py       # 主扫描脚本
├── requirements.txt         # Python依赖
├── .env.example            # 环境变量配置示例
├── .gitignore              # Git忽略文件
└── README.md               # 说明文档
```

## 🚀 快速开始

### 1. Fork本仓库

点击右上角的"Fork"按钮，将这个项目复制到你自己的GitHub账号下。

### 2. 配置GitHub Secrets

进入你的仓库 Settings > Secrets and variables > Actions，添加以下Secrets：

#### 邮件通知（推荐）
- `SMTP_HOST`: SMTP服务器地址（如：smtp.gmail.com）
- `SMTP_PORT`: SMTP端口（如：587）
- `SENDER_EMAIL`: 发件人邮箱
- `SENDER_PASSWORD`: 邮箱授权码/应用密码
- `RECEIVER_EMAIL`: 收件人邮箱

#### 钉钉通知
- `DINGTALK_WEBHOOK`: 钉钉机器人Webhook地址
  - 在钉钉群中添加自定义机器人，获取Webhook地址

#### 企业微信通知
- `WECHAT_WORK_WEBHOOK`: 企业微信机器人Webhook地址
  - 在企业微信群中添加机器人，获取Webhook地址

#### Server酱通知
- `SERVERCHAN_SENDKEY`: Server酱的SendKey
  - 访问 sct.ftqq.com 获取SendKey

### 3. 启用GitHub Actions

- 进入仓库的 Actions 标签页
- 如果看到提示，点击"I understand my workflows, go ahead and enable them"
- 工作流会自动运行，也可以手动触发测试

### 4. 手动测试

进入 Actions 标签页，选择"可转债申购提醒"工作流，点击"Run workflow"手动运行测试。

## ⚙️ 本地运行（可选）

如果你想在本地运行测试：

```bash
# 克隆仓库
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填写你的配置

# 运行脚本
python check_new_bonds.py
```

## 📊 工作原理

1. **定时触发**：GitHub Actions每天UTC时间0:00（北京时间8:00）自动运行
2. **数据获取**：从东方财富网获取当日可转债申购数据
3. **消息推送**：通过配置的渠道发送通知
4. **结果保存**：扫描结果保存为JSON文件，可在Artifacts中查看

## 🔧 自定义配置

### 修改运行时间

编辑 `.github/workflows/check_bonds.yml` 文件：

```yaml
schedule:
  - cron: '0 0 * * 1-5'  # 修改为需要的cron表达式
```

Cron表达式格式：`分 时 日 月 星期`

### 添加更多通知方式

可以在 `check_new_bonds.py` 中添加更多通知方式，如：

- 飞书机器人
- Telegram Bot
- Slack Webhook
- 短信API

## 📈 通知示例

### 有新股申购时
```
🎉 2024-01-17 今日有 2 只可转债可申购！

1. 金现转债 (123456)
   申购日期: 2024-01-17

2. 银轮转债 (654321)
   申购日期: 2024-01-17

记得今日申购哦！💰
```

### 无新股时
```
📊 2024-01-17 今日无可转债申购
```

## 🛡️ 注意事项

1. **GitHub Actions额度**：免费账户每月有2000分钟运行时间，本项目每次运行约1-2分钟
2. **数据准确性**：数据来源于公开网络，建议申购前再次核实
3. **网络问题**：如果数据获取失败，会尝试备用数据源
4. **节假日**：建议手动关闭节假日的工作流运行

## 🔍 故障排查

### 工作流运行失败

1. 检查Secrets是否配置正确
2. 查看Actions日志，确认错误信息
3. 检查网络连接是否正常

### 收不到通知

1. 确认至少配置了一种通知方式
2. 检查通知服务的配置是否正确
3. 查看垃圾邮件文件夹（邮件通知）
4. 确认GitHub Actions运行成功

## 📄 开源协议

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 支持

如有问题，请在GitHub Issues中提出。

---

**免责声明**：本项目仅供学习交流使用，投资有风险，申购需谨慎。
