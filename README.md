# 综测计算器

bnu 学业成绩处理系统,用于应对综测分数计算期间教务给的垃圾成绩单文件(服了),志在减轻各位班长的工作压力

## 目录结构

```
.
├── data/                # 存放输入数据的目录
│   └── *.xls           # 需要处理的Excel文件
├── out/                 # 输出结果的目录
│   └── *.json          # 生成的JSON文件
├── data_processor.py    # 数据处理的主要逻辑
└── main.py              # 主程序入口
```

安装依赖
确保您的环境中已安装以下依赖：
`BeautifulSoup4`
`lxml`
您可以通过以下命令安装所需的库：

```bash
pip install beautifulsoup4 lxml


```

使用方法
将成绩单文件放入 data/ 目录中。
在命令行中运行主程序：

```bash
python main.py
```

## 功能

- 读取表格数据：从指定目录中读取所有 Excel 文件中的表格项。
- 处理课程数据：根据读取的数据构建课程对象和学生对象，并计算学生成绩。
- 输出 JSON 文件：将处理后的专业及课程信息保存为 JSON 格式，以便后续使用。

## 数据结构

## 课程类 (Course)

- name: 课程名称
- credits: 课程学分
- type: 课程类型（必修或选修）

## 学生类 (Student)

- index: 学生索引
- name: 学生姓名
- student_id: 学号
- scores: 课程成绩列表
- has_failed_course: 是否有不及格课程

## 专业类 (Major)

- grade: 年级
- name: 专业名称
- courses: 课程列表
- students: 学生列表

## 贡献

欢迎提交问题和请求功能。如果您对这个项目有任何改进建议，请提出您的意见！

## 许可

该项目使用 MIT 许可证，详细信息请查看 LICENSE 文件。

Feel free to customize any sections or details according to your project's specifics!
