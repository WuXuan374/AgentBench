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
## 找到 KBQA 相关的文件，同时删除其他应用的相关文件
- 修改 start_task.yaml, 里面仅执行 KBQA 任务
- 修改 start_task 任务里面的其他参数
    - base-port 选择一个比较特殊的，避免冲突
- 暂时把 worker 数量设置为 1
```shell
python -m src.start_task -a
```
- controller 的端口始终是 5000, base-port 参数设置的是 worker 的起始端口
### 执行 kg task
- 调用的是 tasks.knowledgegraph.KnowledgeGraph 模块
- 我们打一些断点 (需要 Debug task server 才能走到这些断点)
- 框架封装了对于大模型返回结果的解析，并且能够调用 api.py 里面定义的函数
### 启动 assinger, 执行 KBQA 任务
- assignment/default.yaml 中需要修改的内容较多
    - task 只有 KBQA
    - agent 使用 ernie-bot
- assignment/definition.yaml:
```controller_address: "http://114.212.190.19:5000/api"``
    - 发现 0.0.0.0 或者 localhost 都访问不同，记得之前了解过，好像是 VSCode 的 forwarding 问题
- 最好加上 -r 参数，auto-retry
```bash
python -m src.assigner
```

# 代码学习
- http_agent.py: 访问大模型提供的 HTTP 接口
    - Prompter: 历史对话记录
    - 更完善的错误处理机制: 重试机制、context limit
    - 超时时间我觉得可以设置一下，如果使用 ernie-bot, 默认超时时间可以设置为 0
- async