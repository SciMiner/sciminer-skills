# SciMiner 中文技能海报

独立的中文海报套件，对应根目录 [posters](../posters) 中的英文版，不会改动现有英文页面。

## 文件

- `index.html`：14 张中文海报总览页
- `hero.html`：SciMiner 总览海报
- `<skill>.html`：13 张单技能海报
- `styles.css`：共享样式
- `generate.py`：重新生成全部中文海报

## 预览

```bash
cd posters-zh-CN
python3 -m http.server 8766
# 然后打开 http://127.0.0.1:8766/index.html
```

手机上每张海报会铺满整个屏幕；桌面端会以手机外框形式展示。

## 重新生成

```bash
cd posters-zh-CN
python3 generate.py
```

运行后会重写全部中文 HTML 海报，`styles.css` 和 `README.md` 不会被覆盖。