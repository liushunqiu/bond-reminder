# GitHub Secrets 配置指南

## Server酱配置已测试成功！✓

你的Server酱SendKey已配置并测试成功！

### 本地配置
- ✅ `.env` 文件已创建
- ✅ Server酱SendKey已添加
- ✅ 通知测试成功

### GitHub配置步骤

#### 1. 创建GitHub仓库
1. 访问 https://github.com/new
2. 创建新仓库（仓库名：`bond-reminder` 或任意名称）
3. 勾选 "Public" 或 "Private"
4. 点击 "Create repository"

#### 2. 添加GitHub Secrets
1. 进入你的GitHub仓库
2. 点击 `Settings` > `Secrets and variables` > `Actions`
3. 点击 `New repository secret`
4. 添加以下Secret：

**Secret名称**: `SERVERCHAN_SENDKEY`
**Secret值**: `SCT127853TnWQdkFXAGrR78EpKTMa3dXwh`
5. 点击 `Add secret`

#### 3. 推送代码到GitHub
```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: 可转债申购提醒系统"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 推送
git push -u origin main
```

#### 4. 启用GitHub Actions
1. 进入仓库的 `Actions` 标签页
2. 如果看到提示，点击 "I understand my workflows, go ahead and enable them"
3. 点击左侧的 `可转债申购提醒`
4. 点击 `Run workflow` > `Run workflow` 手动运行测试

#### 5. 验证通知
1. 等待工作流运行完成
2. 检查你的手机是否收到Server酱通知
3. 查看Actions运行日志确认成功

## 自动化运行

配置完成后，系统将：
- ✅ 每天早上8点（北京时间）自动运行
- ✅ 检查当天是否有可转债申购
- ✅ 通过Server酱发送通知到你的手机
- ✅ 工作日总是通知，周末无数据时跳过通知

## 测试命令

本地测试：
```bash
# 测试今天
python check_new_bonds.py

# 测试特定日期
python test_2026_01_16.py

# 测试Server酱通知
python test_serverchan.py
```

## 完成！

配置完成后，你将每天早上8点自动收到可转债申购提醒！🎉