# Photo to Line Art · 照片转排线画

纯前端照片转排线艺术工具。图片仅在浏览器处理，无 API、无后端、无注册和水印。

## 功能
- 点击或拖放 JPG / PNG / WebP（最大 10 MB）
- 斜向、交叉、水平、垂直四种排线
- 密度、粗细、对比度、线条色与背景色调整
- 原图对比、重置、PNG 导出
- 内置程序绘制示例；手机布局

## 本地运行
直接打开 index.html，或在项目目录运行 `python -m http.server 8080`，访问 http://localhost:8080。

## 部署
### GitHub Pages
仓库 Settings → Pages → Deploy from a branch → main / (root) → Save。
预计地址：https://colddcc.github.io/photo-to-line-art/ （需自行启用 Pages，当前不代表已上线）。

### Cloudflare Pages
导入本仓库；Framework preset 选 None；Build command 留空；Build output directory 填 `.`。
这是静态项目，无需 npm install 或构建命令。

## 文件
- index.html：页面与元信息
- styles.css：桌面和移动端样式
- app.js：示例图、亮度采样、排线与导出
- favicon.svg：图标

## 算法与限制
沿平行路径采样亮度，按暗度改变线宽；交叉模式在暗部叠加第二方向。不会将原照片直接叠在输出下方。
预览长边最高 900 px，上传处理长边最高 2400 px，导出长边最高 2000 px，不放大小图。
原图色彩模式为实验功能，后续再优化。当前不是轮廓提取或沿物体结构走向的智能线稿。
参数处理在主线程进行，大图高清导出可能短暂卡顿；后续可改为 Worker。

## 后续修改
仓库：https://github.com/COLDDCC/photo-to-line-art
已确认的基础排线效果优先保留，色彩增强后续进行。

## 多语言
支持 English、简体中文、日本語、Español、Português、한국어，默认英文。
选择优先级：有效的 `?lang=` 参数 → 本地保存的选择 → 浏览器语言偏好 → 英文。
语言代码为 `en`、`zh-CN`、`ja`、`es`、`pt`、`ko`。例如 `?lang=ja` 可直接打开日文界面。
手动切换会记住偏好，保留上传图片与参数，并更新分享链接。禁用本地存储时仍可使用浏览器语言与链接参数。
不进行 IP 查询、不调用地理位置 API。当前为同一页面的多语言界面，尚非独立可索引的多语言 SEO 页面。
翻译位于 `i18n.js`。新增语言时需补齐所有键与语言下拉选项。
