---
type: network_behavior
os: windows
app: "[[Windows Service Host]]"
process: "[[svchost.exe]]"
protocol: [tcp, udp, rpc, dns]
purpose: "系统管理、用户交互、服务承载或组件网络访问"
risk_level: medium
confidence: medium
status: active
tags:
  - network/windows-app-profile
source_row_ids:
  - win-builtin-001
  - win-builtin-002
  - win-builtin-003
  - win-builtin-004
  - win-builtin-005
  - win-builtin-006
  - win-builtin-007
  - win-builtin-008
  - win-builtin-009
  - win-builtin-010
  - win-builtin-011
  - win-builtin-012
  - win-builtin-013
  - win-builtin-014
  - win-builtin-015
  - win-builtin-016
  - win-builtin-017
  - win-builtin-018
  - win-builtin-019
  - win-builtin-020
  - win-builtin-021
  - win-builtin-022
  - win-builtin-023
  - win-builtin-024
  - win-builtin-025
  - win-builtin-026
  - win-builtin-027
  - win-builtin-028
  - win-builtin-029
  - win-builtin-030
  - win-builtin-031
  - win-builtin-032
  - win-builtin-033
  - win-builtin-034
  - win-builtin-035
  - win-builtin-036
  - win-builtin-037
  - win-builtin-038
  - win-builtin-039
  - win-builtin-040
  - win-builtin-041
  - win-builtin-042
  - win-builtin-043
  - win-builtin-044
  - win-builtin-045
  - win-builtin-046
  - win-builtin-047
  - win-builtin-048
  - win-builtin-049
  - win-builtin-050
  - win-builtin-051
  - win-builtin-052
  - win-builtin-053
  - win-builtin-054
  - win-builtin-055
  - win-builtin-056
  - win-builtin-057
  - win-builtin-058
  - win-builtin-059
  - win-builtin-060
  - win-builtin-061
  - win-builtin-062
  - win-builtin-063
  - win-builtin-064
  - win-builtin-065
  - win-builtin-066
  - win-builtin-067
  - win-builtin-068
  - win-builtin-069
  - win-builtin-070
  - win-builtin-071
  - win-builtin-072
  - win-builtin-073
  - win-builtin-074
  - win-builtin-075
  - win-builtin-076
  - win-builtin-077
  - win-builtin-078
  - win-builtin-079
  - win-builtin-080
  - win-builtin-081
  - win-builtin-082
  - win-builtin-083
  - win-builtin-084
  - win-builtin-085
  - win-builtin-086
  - win-builtin-087
  - win-builtin-088
  - win-builtin-089
  - win-builtin-090
  - win-builtin-091
  - win-builtin-092
  - win-builtin-093
  - win-builtin-094
  - win-builtin-095
  - win-builtin-096
  - win-builtin-097
  - win-builtin-098
  - win-builtin-099
  - win-builtin-100
  - win-builtin-101
  - win-builtin-102
  - win-builtin-103
  - win-builtin-104
  - win-builtin-105
  - win-builtin-106
  - win-builtin-107
  - win-builtin-108
  - win-builtin-109
  - win-builtin-110
  - win-builtin-111
  - win-builtin-112
  - win-builtin-113
  - win-builtin-114
  - win-builtin-115
  - win-builtin-116
  - win-builtin-117
  - win-builtin-118
  - win-builtin-119
  - win-builtin-120
  - win-builtin-121
  - win-builtin-122
  - win-builtin-123
  - win-builtin-124
  - win-builtin-125
  - win-builtin-126
  - win-builtin-127
  - win-builtin-128
  - win-builtin-129
  - win-builtin-130
  - win-builtin-131
  - win-builtin-132
  - win-builtin-133
  - win-builtin-134
  - win-builtin-135
  - win-builtin-136
  - win-builtin-137
  - win-builtin-138
  - win-builtin-139
  - win-builtin-140
  - win-builtin-141
  - win-builtin-142
  - win-builtin-143
  - win-builtin-144
  - win-builtin-145
  - win-builtin-146
  - win-builtin-147
  - win-builtin-148
  - win-builtin-149
  - win-builtin-150
  - win-builtin-151
  - win-builtin-152
  - win-builtin-153
  - win-builtin-154
  - win-builtin-155
  - win-builtin-156
  - win-builtin-157
  - win-builtin-158
  - win-builtin-159
  - win-builtin-160
  - win-builtin-161
  - win-builtin-162
  - win-builtin-163
  - win-builtin-164
  - win-builtin-165
  - win-builtin-166
  - win-builtin-167
  - win-builtin-168
  - win-builtin-169
  - win-builtin-170
  - win-builtin-171
  - win-builtin-172
  - win-builtin-173
  - win-builtin-174
  - win-builtin-175
  - win-builtin-176
  - win-builtin-177
  - win-builtin-178
  - win-builtin-179
  - win-builtin-180
  - win-builtin-181
  - win-builtin-182
  - win-builtin-183
  - win-builtin-184
  - win-builtin-185
  - win-builtin-186
  - win-builtin-187
  - win-builtin-188
  - win-builtin-189
  - win-builtin-190
  - win-builtin-191
  - win-builtin-192
  - win-builtin-193
  - win-builtin-194
  - win-builtin-195
  - win-builtin-196
  - win-builtin-197
  - win-builtin-198
  - win-builtin-199
  - win-builtin-200
  - win-builtin-201
  - win-builtin-202
  - win-builtin-203
  - win-builtin-204
  - win-builtin-205
  - win-builtin-206
  - win-builtin-207
  - win-builtin-208
  - win-builtin-209
  - win-builtin-210
  - win-builtin-211
  - win-builtin-212
  - win-builtin-213
  - win-builtin-214
  - win-builtin-215
  - win-builtin-216
  - win-builtin-217
  - win-builtin-218
  - win-builtin-219
  - win-builtin-220
  - win-builtin-221
  - win-builtin-222
  - win-builtin-223
  - win-builtin-224
  - win-builtin-225
  - win-builtin-226
  - win-builtin-227
  - win-builtin-228
  - win-builtin-229
  - win-builtin-230
  - win-builtin-231
  - win-builtin-232
  - win-builtin-233
---
# Windows Service Host 网络行为

<!-- generated: windows-complete-profile-backfill -->

## 1. 行为说明

本页描述 [[Windows Service Host]] 的常见网络行为模式。精确域名和网关必须来自官方文档、企业资产台账、代理日志、EDR/Sysmon 或流量观测，不在无来源情况下硬编码。

## 2. 相关进程

- [[svchost.exe]]

## 3. 常见端口

```text
depends-on-hosted-service
```

## 4. 常见目标

```text
厂商云服务、企业管理端、授权服务器、更新源、业务数据库或内网网关。
不要无来源填充精确域名、IP、账号或租户标识。
```

## 5. 正常用途

目的地址与企业授权、厂商服务或业务系统一致，路径、签名和启动账户可信。

## 6. 异常关注点

```text
系统组件从异常路径启动、由异常父进程拉起或产生与职责不符的外联。
进程路径、签名、父进程、启动账户或服务 ImagePath 与应用画像不一致
网络连接出现在未授权资产、异常时间窗口或异常登录之后
```

## 7. 关联对象

- [[Windows Service Host]]
- [[应用异常网络外联行为]]
- [[Windows常见应用完整画像验收清单]]
