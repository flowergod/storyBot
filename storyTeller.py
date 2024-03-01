import os
import requests
import openai
import csv
from datetime import datetime, date
import logging
 
# 配置日志记录器
logger = logging.getLogger()
logger.setLevel(logging.INFO) # 设置日志等级为 INFO
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # 定义日志格式
console_handler = logging.StreamHandler() # 创建控制台处理程序
console_handler.setLevel(logging.INFO) # 设置控制台处理程序的日志等级
console_handler.setFormatter(formatter) # 设置控制台处理程序的日志格式
logger.addHandler(console_handler) # 添加控制台处理程序到日志记录器
 

# 设置OpenAI API密钥
key = "sk-HX50YjivKlGN2y0zCbA60e840cE04941A1Eb23Be4fDa4a88"
model="gpt-3.5-turbo"

storyFile = '.\\storyBot\\stories.csv'

# 生成故事
def generate_story(key, msg, model):
    openai.api_key = os.getenv('OPENAI_KEY', default=key)
    openai.api_base = "https://ai-yyds.com/v1"
    
    messages = msg

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=1.0,
    )
    result = ''
    for choice in response.choices:
        result += choice.message.content

    return result

# 更新故事
def update_story_file(story):
    # 获取当前日期
    today = date.today()

    # 打开CSV文件
    with open(storyFile, 'r', encoding='utf-8') as file:
        # 读取CSV文件内容
        csv_reader = csv.reader(file)
        # 将CSV内容转换为列表
        rows = list(csv_reader)

    # 判断是否有当天的数据
    today_data = None
    
    date_format = '%Y-%m-%d'

    for row in rows[1:]:
        row_date = datetime.strptime(row[0], '%Y-%m-%d').date()
        if row_date == today:
            today_data = row
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
    
    # 如果有当天的数据，更新当前date列的data
    if today_data:
        today_data[1] = processed_story
    # 如果没有当天的数据，新增一条，date是今天
    else:
        new_row = [today.strftime('%Y-%m-%d'),  processed_story]
        rows.append(new_row)

    # 将修改后的内容写回CSV文件
    with open(storyFile, 'w', newline='', encoding='utf-8') as file:
        # 创建CSV写入对象
        csv_writer = csv.writer(file)
        # 逐行写入CSV内容
        csv_writer.writerows(rows)


def main():
    messages = [
        {"role": "system", "content": "你是一个优秀的作家，擅长用温馨的文字书写动人的故事"},    
        {"role": "user", "content": "请为我写一个温馨、有爱的晚安小故事"},
    ]

    logger.info("正在写故事...")
    story = generate_story(key, messages, model)
    
    update_story_file(story)
    logger.info("故事写好了，去看看吧，愿你拥有美好的一天")

if __name__ == '__main__':
   main()

'''
    with open(storyFile, 'r') as file:
        # 读取CSV文件内容
        csv_reader = csv.reader(file)
        # 将CSV内容转换为列表
        rows = list(csv_reader)
    
    print(rows[1])
'''





