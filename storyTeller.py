import openai
import csv
from datetime import datetime, date, timedelta
 
# 配置日志记录器
# logger = logging.getLogger()
# logger.setLevel(logging.INFO) # 设置日志等级为 INFO
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s') # 定义日志格式
# console_handler = logging.StreamHandler() # 创建控制台处理程序
# console_handler.setLevel(logging.INFO) # 设置控制台处理程序的日志等级
# console_handler.setFormatter(formatter) # 设置控制台处理程序的日志格式
# logger.addHandler(console_handler) # 添加控制台处理程序到日志记录器
 

# 设置OpenAI API密钥
key = "sk-K231s4pXBHfHz76KNxzBfJxCAWV0V6oAm1L6z8QC8LmkYyLk"
model="moonshot-v1-8k"

storyFile = 'stories.csv'

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
    
    # 如果有当天的数据，更新当前date列的data
    if story_date_data:
        story_date_data[1] = processed_story
    # 如果没有当天的数据，新增一条，date是今天
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
        {"role": "system", "content": "你是一个优秀的作家，擅长用温馨的文字书写动人的故事"},    
        {"role": "user", "content": "请为我写一个温馨、有爱的晚安小故事"},
    ]

    # logger.info("正在写故事...")
    story = generate_story(key, messages, model)
    
    update_story_file(story)
    # logger.info("故事写好了，去看看吧，愿你拥有美好的一天")

def update_story_till_today():
    messages = [
        {"role": "system", "content": "你是一个优秀的作家，擅长用温馨的文字书写动人的故事"},    
        {"role": "user", "content": "请为我写一个温馨、有爱的晚安小故事"},
    ]
    # 设置起始日期为今年的3月1日
    start_date = datetime(datetime.today().year, 3, 1)

    # 获取今天的日期
    end_date = datetime.today()

    # 确保结束日期不早于开始日期
    if end_date < start_date:
        print("End date is before start date. Please check the dates.")
    else:
        # 循环调用update_story函数
        current_date = start_date
        while current_date <= end_date:
            update_story_file(generate_story(key, messages, model), current_date)
            # 增加一天进入下一次循环
            current_date += timedelta(days=1)


if __name__ == '__main__':
   update_story_till_today()





