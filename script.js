let currentOpenStory = null; // 添加一个变量来跟踪当前展开的故事元素

// 读取CSV文件
fetch("stories.csv")
  .then((response) => response.text())
  .then((data) => {
    // 将CSV数据转换为数组
    const rows = data.split("\n").slice(1);
    const stories = rows.map((row) => {
      const [date, story] = row.split(",");
      return { date, story };
    });

    // 按照时间倒序排列历史故事列表
    stories.sort((a, b) => new Date(b.date) - new Date(a.date));

    // 显示最新的故事
    document.getElementById("latest-story-text").innerHTML = stories[0].story;
    // 设置最新故事的日期
    document.getElementById("date").textContent = stories[0].date;

    // 显示历史故事列表
    const historyList = document.getElementById("history-list");
    const storyElements = []; // 创建故事元素的数组

    stories.splice(0, 1);

    stories.forEach((story) => {
      const dateEl = document.createElement("div");
      dateEl.classList.add("date");
      dateEl.textContent = story.date;
      dateEl.addEventListener("click", () => {
        // 如果当前有展开的故事，先将其关闭
        if (
          currentOpenStory &&
          currentOpenStory !== dateEl.nextElementSibling
        ) {
          currentOpenStory.style.display = "none";
        }

        // 切换当前点击的故事的显示状态
        const storyEl = dateEl.nextElementSibling;
        if (storyEl.style.display === "none") {
          storyEl.style.display = "block";
          currentOpenStory = storyEl; // 更新当前展开的故事元素
        } else {
          storyEl.style.display = "none";
          currentOpenStory = null; // 如果故事被关闭，重置当前展开的故事元素
        }
      });
      const storyEl = document.createElement("div");
      storyEl.classList.add("story");
      storyEl.innerHTML = story.story;
      storyEl.style.display = "none";

      historyList.appendChild(dateEl);
      historyList.appendChild(storyEl);

      storyElements.push({
        date: new Date(story.date),
        element: dateEl.parentNode,
      }); // 添加故事元素到数组中
    });
  });

async function main() {
  const apiKey = "sk-K231s4pXBHfHz76KNxzBfJxCAWV0V6oAm1L6z8QC8LmkYyLk"; // 替换为你的 OpenAI API 密钥
  const model = "moonshot-v1-8k"; // 替换为你使用的模型
  const apiUrl = "https://api.moonshot.cn/v1/chat/completions";
  const themeInput = document.getElementById("story-theme");
  const storyOutput = document.getElementById("story-output");

  const theme = themeInput.value; // 获取用户输入的主题

  storyOutput.textContent = "开始写故事...";

  if (!theme) {
    storyOutput.textContent = "请提供一个故事主题";
    return;
  }

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: model,
        messages: [
          {
            role: "system",
            content:
              "你是一个优秀的作家，擅长根据各类主题，撰写出色的故事。故事要求1000字以上。请用以下格式返回结果：故事题目（不要出现“故事题目”这4个字）  <br> <br> --- <br> <br> 故事正文 <br> <br> --- <br> <br> ",
          },
          {
            role: "user",
            content: `请以 "${theme}" 为主题，为我写一个故事。`,
          },
        ],
        temperature: 0.3,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      const errorMessage = errorData.error.message;
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorMessage}`
      );
    }

    const data = await response.json();
    storyOutput.innerHTML = data.choices[0].message.content;
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
    storyOutput.textContent = `无法加载故事：${error.message}`; // 将错误信息显示在页面上
  }
}

// 页面加载完成后，为按钮添加点击事件监听器
document.addEventListener("DOMContentLoaded", () => {
  const generateStoryButton = document.getElementById("generate-story-btn");
  if (generateStoryButton) {
    generateStoryButton.addEventListener("click", main);
  }
});
