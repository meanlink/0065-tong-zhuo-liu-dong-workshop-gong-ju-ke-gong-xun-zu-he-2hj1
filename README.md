# 同桌 · 流动工坊工具课共训组合

绕城流动工坊有三名带教员，为三个社区安排入门课堂。联用选题原先靠回忆，常混入失效学员卡、忽略共同出席人数，或到驻点才发现教具不够。系统使用签到与回收观察单，输出共训教案给巡回驻点。

## 一天的工作顺序

1. 09:00 核对五门课程的教具盘点。
2. 09:30 确认 P01 当天已收回观察单。
3. 10:00 P07 临访卡已过期，记录不进入共训。
4. 11:10 按共同人数至少 2 人、相似度至少 0.6 计算。
5. 12:40 查看 FOLD 和 LABEL 的 3 人重叠。
6. 13:10 渡头 DT2 教具只有 1 套，联合教案拒绝。
7. 14:15 许家巷 XS1 签发 22 分钟、2 套教具的教案。

## 算法口径

按课程建立有效已签收学员集合。两课程 Jaccard 为交集人数除以并集人数；同时满足相似度和交集人数下限才连边。以图的连通分量作为组合，并保留每条支持边。连通组合中的课程可能通过其他课程间接连接。

## 合卡

学员补卡后，同一学员的两张卡会在共训页面合成一张：副卡签到归正卡，同课同日有一张已签收就算签收，之后用副卡补录的签到也记到正卡。合卡与补录互斥不丢记录，重复合卡不重复计人。合卡后按上次成功计算的门槛自动重算组合；重算期间暂停签发新教案，算完恢复，失败保留旧版组合供查。共训页面顶部标出"停签中 / 签发已恢复"状态。

## 上手

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
docker compose down --remove-orphans
```

前端走本机 **18459**，API 走 **19459**，PostgreSQL 走 **17959**。本地开发可在安装 Python 3.11、PostgreSQL 和 Redis 后配置与 Compose 相同的环境变量，在 backend 运行 `uvicorn app:app --reload`，前端以 Nginx 同源代理启动。

| 角色 | 邮箱 | 业务权限 |
|---|---|---|
| 录入员 | operator@demo.local | 收回观察单、计算分组 |
| 复核员 | reviewer@demo.local | 核对驻点资源、签发教案 |
| 查阅员 | viewer@demo.local | 查课程、签到和外出教案 |

三个演示账号默认密码均为 `Demo2026!`。使用本地合成样本，seed 只插入缺失的自然键。关闭 `SEED_DEMO` 可跳过自动 seed。使用自己的 `JWT_SECRET`、`POSTGRES_PASSWORD` 和 `DEMO_PASSWORD` 部署。

| 目录 | 技术与职责 |
|---|---|
| backend | Python 3.11 / FastAPI，使用 PostgreSQL 16；Worker 轮询持久化队列，Redis 为登录限流及健康检查提供支持 |
| frontend | Nginx、HTML、CSS、JavaScript ES modules，HTTP 同源代理 |
| docker-compose.yml | 5 服务及健康检查、独立卷；Redis 与 worker 无宿主端口 |

角色、作业状态在 `backend/core.py`、`frontend/base.js` 定义，在 `backend/core.py`（鉴权、队列）与 `backend/worker.py` 使用。领域阶段由数据库约束与业务服务维护，`frontend/view.js` 负责显示。接口输出为最新已提交状态。

观察单与签到样本为合成记录。本演示不连接外部排课或消息系统。

MIT License
