# 快速配置指南（5分钟完成）

## 第一步：配置GitHub Secrets

进入你的GitHub仓库：`Settings` > `Secrets and variables` > `Actions` > `New repository secret`

### 方式1：邮件通知（最推荐）

使用QQ邮箱示例：

| Secret名称 | 值 | 说明 |
|-----------|-----|------|
| `SMTP_HOST` | `smtp.qq.com` | QQ邮箱SMTP服务器 |
| `SMTP_PORT` | `587` | 端口号 |
| `SENDER_EMAIL` | `your_qq@qq.com` | 你的QQ邮箱 |
| `SENDER_PASSWORD` | `your_auth_code` | **注意：不是邮箱密码！是授权码** |
| `RECEIVER_EMAIL` | `your_phone@139.com` | 接收通知的邮箱（可发短信） |

**如何获取QQ邮箱授权码？**
1. 登录QQ邮箱
2. 进入 `设置` > `账户` 
3. 找到 `POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务`
4. 开启 `POP3/SMTP服务`
5. 发送短信获取授权码

**接收邮箱推荐：**
- 移动：`your_phone@139.com` (免费短信通知)
- 联通：`your_phone@wo.cn`
- 电信：`your_phone@189.cn`

### 方式2：钉钉通知

1. 在钉钉群里添加自定义机器人
2. 获取Webhook地址（格式：`https://oapi.dingtalk.com/robot/send?access_token=xxx`）
3. 添加Secret：`DINGTALK_WEBHOOK` = 你的Webhook地址

### 方式3：企业微信通知

1. 在企业微信群中添加机器人
2. 获取Webhook地址（格式：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx`）
3. 添加Secret：`WECHAT_WORK_WEBHOOK` = 你的Webhook地址

### 方式4：Server酱（最简单）

1. 访问 `sct.ftqq.com`
2. 用GitHub账号登录，获取SendKey
3. 添加Secret：`SERVERCHAN_SENDKEY` = 你的SendKey
4. 关注微信公众号接收通知

## 第二步：测试配置

手动运行工作流测试：

1. 进入仓库的 `Actions` 标签页
2. 点击左侧的 `可转债申购提醒`
3. 点击右侧的 `Run workflow`
4. 等待运行完成，查看是否收到通知

## 第三步：完成！

系统会自动在每个工作日的早上8点（北京时间）运行，扫描当天是否有可转债申购。

有新股时会收到通知，无新股时不会打扰你。

---

## 常见问题

### Q: 没有收到通知怎么办？
A: 
1. 检查GitHub Actions是否运行成功
2. 查看Actions日志确认是否有错误
3. 检查垃圾邮件文件夹
4. 确认配置信息正确

### Q: 如何修改运行时间？
A: 编辑 `.github/workflows/check_bonds.yml` 文件中的 `cron` 表达式

### Q: 周末也会运行吗？
A: 默认只在工作日运行（周一到周五），可在配置文件中修改

### Q: 支持哪些邮箱？
A: 支持所有支持SMTP的邮箱（QQ、163、Gmail、Outlook等）

---

**配置完成后，建议手动运行一次测试，确保能正常收到通知！**
