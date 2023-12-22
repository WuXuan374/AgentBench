# 基本代码结构
- configs
    - agents: 各类 API 的配置文件
- src
    - start_task.py: 总入口
        - 看起来不是所有任务都需要 docker

# 整体框架
- Task Server: host a task environment
    - 平常 QA 时候的 Virtuoso endpoint
    - Controller: 
        - 底下有多个 Worker, 应该是出于效率考虑
        - 实现服务转发，负载均衡等功能
- Agent Server: Agent interface, 可以 infer from historical data?
    - 大模型访问接口 --> 主要针对开源大模型，我们可以忽略
- Client
    - 大模型返回结果的 parsing, 使用等？
    - Assigner: 并发控制，比如 test case 的分配

# 入口函数
- `src.server.task_controller`: task server 核心，管理所有的 task_worker, 默认在 5000 端口 （可以手动指定）
- `src.start_task`: 读取配置文件，启动 task_worker
- `src.assigner`: 效果评测

# conda 环境
- agent-bench: /home/home2/xwu/.conda/envs/agent-bench

# 复现过程
## 尝试将 gpt-3.5 替换成 ernie-bot
- 需要在 agents 目录下新增一个 ernie-bot 的配置文件
- HTTPAgent
    - 实现的泛化性非常好! ernie-bot 只需要修改配置文件就够了!