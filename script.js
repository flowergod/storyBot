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

document.addEventListener("DOMContentLoaded", () => {
  async function main() {
    document.getElementById("story-output").textContent = "开始写故事...";

    try {
      const apiKey = "sk-K231s4pXBHfHz76KNxzBfJxCAWV0V6oAm1L6z8QC8LmkYyLk";
      const response = await fetch(
        "https://api.moonshot.cn/v1/chat/completions",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            model: "moonshot-v1-8k",
            messages: [
              {
                role: "system",
                content: "你是一个优秀的作家，擅长用温馨的文字书写动人的故事。",
              },
              { role: "user", content: "请为我写一个温馨、有爱的晚安小故事。" + "请用以下格式返回结果：故事题目（不要出现“故事题目”这4个字）  <br> <br> --- <br> <br> <故事正文> <br> <br> --- <br> <br> 故事讲完了。你觉得怎么样？" },
            ],
            temperature: 0.3,
          }),
        }
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      document.getElementById("story-output").innerHTML =
        data.choices[0].message.content;
    } catch (error) {
      console.error(
        "There has been a problem with your fetch operation:",
        error
      );
      document.getElementById("story-output").textContent =
        error;
    }
  }

  const generateStoryButton = document.getElementById("generate-story-btn");
  if (generateStoryButton) {
    generateStoryButton.addEventListener("click", main);
  } else {
    console.error("Generate story button not found");
  }
});
