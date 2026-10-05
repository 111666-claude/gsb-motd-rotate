# motd-rotate

登录公告轮播：按 tick 推进时间，每个 tick 选一条公告播出。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m motd run --announcements a.json --ticks 5 --start 0 --step 30000
python3 -m motd --sample=window|pin|weight|replay|work
```

公告字段：`id`、`weight`、`start`、`end`、`pinned`。

## 口径

- **时间窗口**：公告只在 `[start, end)` 内可播，越界的一律不参与。
- **覆盖层**：处于置顶（`pinned`）状态且在当前窗口内的公告优先播出，且不消耗轮转位。
- **权重轮转**：可播公告按 `weight` 在轮转环里占位，同一条重复 `weight` 次，按 `id` 升序拼接；每结算一个 tick 前进一位。
- **幂等**：同一个 tick 只结算一次；重复请求返回同一结果，轮转位不再前进。

## 不变量

- 每次选中的公告都处于它自己的窗口内。
- 同一个 tick 无论结算几次，结果都一样。
- `scanned` 不随 tick 数放大：3000 个 tick 的 `scanned` 不超过 12000。

## 输出契约

每个 tick 打印一行 JSON：`tick`、`id`（没有可播公告时为 null）、`status`（`ok` / `replay`）、`scanned`。

`--sample=work` 只打印 `{"ticks": N, "scanned": N}`。
