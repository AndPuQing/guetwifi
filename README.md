## GUET-WIFI 自动登录

### 使用说明

导入requests库
按如下填入参数

-a：账号

-p：密码

-o：运营商（可选，默认校园网）[cmcc,telecom,unicom]

-d：设备（可选，默认pc端）[pc,phone]

### 异常说明

- 出现AC校验失败->重连网络
- 账号已登录->已有相同ip上线，在管理系统退出登录