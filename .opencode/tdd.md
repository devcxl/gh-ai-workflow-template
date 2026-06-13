# AI Workflow Template — opencode 规则

## 项目
- Python FastAPI 示例项目
- 测试框架: pytest + httpx (TestClient)
- 测试命令: `python -m pytest tests/ -v --tb=short`
- 代码在 app/ 目录，测试在 tests/ 目录

## TDD 循环行为
- RED 阶段: 在 tests/ 下写测试，不修改 app/
- GREEN 阶段: 在 app/ 下实现，不修改 tests/
- 每次迭代先 RED 再 GREEN
- 提交后等待 CI 状态返回结果

## 回复 Issue
- 方案回复用中文
- 方案格式: 需求分析 → 技术方案 → 变更清单 → 测试策略
