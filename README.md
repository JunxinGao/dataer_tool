# dataer_tool
> the tool for dataer


![CI](https://github.com/junxingao/dataer_tool/workflows/CI/badge.svg) ![docs](https://github.com/junxingao/dataer_tool/workflows/docs/badge.svg)

# Develop

## Libray

使用命令 `nbdev_build_lib` 可以生成python库

## Document

如果修改过nbs下面的notebook, 使用命令 `nbdev_build_docs` 可以更新文档

目录映射关系在 `docs/sidebar.json`中可以设置, 首页`index.html`对应的notebook是`nbs/index.ipynb`

# About

This project generate from [nbdev](https://nbdev.fast.ai/)

<details><summary><b>As template</b></summary><blockquote>

~~~
sed -i 's/dataer_tool/YOUR_LIB_NAME/g' `grep -inr dataer_tool -rl .`
mv dataer_tool YOUR_LIB_NAME
~~~
</blockquote></details>
