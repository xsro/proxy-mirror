# Switch Registry and Proxy

修改源或设置镜像

## 用法

```shell
#显示所有支持的工具tool
python main.py [show]
#显示工具tool支持的镜像源
python main.py <tool>
#将工具tool设置为mirror镜像
python main.py <tool> <mirror>
#设置工具tool的代理为proxy
python main.py proxy <tool> <proxy>
#自更新（如果支持）
python main.py update
```