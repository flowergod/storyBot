import openai
import csv
from datetime import datetime, date, timedelta

# 设置OpenAI API密钥
key = "sk-K231s4pXBHfHz76KNxzBfJxCAWV0V6oAm1L6z8QC8LmkYyLk"
model="moonshot-v1-8k"
storyFile = "stories.csv"

# 生成故事
def generate_story(key, msg, model):
    client = openai.OpenAI(
        api_key = key,
        base_url = "https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model = model,
        messages = msg,
        temperature = 0.3,
    )

    result = ''
    for choice in completion.choices:
        result += choice.message.content

    return result

# 更新故事
def update_story_file(story, dt=date.today()):
    # 获取输入日期
    today = dt
    story_date = dt

    # 打开CSV文件
    with open(storyFile, 'r', encoding='utf-8') as file:
        # 读取CSV文件内容
        csv_reader = csv.reader(file)
        # 将CSV内容转换为列表
        rows = list(csv_reader)

    # 判断是否有当天的数据
    story_date_data = None

    for row in rows[1:]:
        row_date = datetime.strptime(row[0], '%Y-%m-%d').date()
        if row_date == story_date:
            story_date_data = row
            break
    
    # 处理story的换行
    processed_story_list = []
    for item in story:
        if "\n" in item:
            # 将换行符转换成其他字符串形式（比如空格）
            processed_item = item.replace("\n", " <br> ")
        else:
            processed_item = item
        
        processed_story_list.append(processed_item)
    processed_story = ''.join(processed_story_list)
    
    # 如果有该日的数据，更新当前date列的data
    if story_date_data:
        story_date_data[1] = processed_story
    # 如果没有该日的数据，新增一条，date是今天
    else:
        new_row = [story_date.strftime('%Y-%m-%d'),  processed_story]
        rows.append(new_row)

    # 将修改后的内容写回CSV文件
    with open(storyFile, 'w', newline='', encoding='utf-8') as file:
        # 创建CSV写入对象
        csv_writer = csv.writer(file)
        # 逐行写入CSV内容
        csv_writer.writerows(rows)


def main():
    messages = [
        {"role": "system", "content": "你是一个优秀的作家，擅长用温馨的文字书写动人的故事。请用以下格式返回结果：故事题目（不要出现“故事题目”这4个字）  <br> <br> --- <br> <br> <故事正文> <br> <br> --- <br> <br> 故事讲完了。愿你有个香甜的梦。晚安。"},    
        {"role": "user", "content": "请为我写一个温馨、有爱的晚安小故事。"},
    ]

    # logger.info("正在写故事...")
    story = generate_story(key, messages, model)
    
    update_story_file(story)
    # logger.info("故事写好了，去看看吧，愿你拥有美好的一天")


if __name__ == '__main__':
   main()





