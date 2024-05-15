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

    stories.slice(0, 10).forEach((story) => {
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

// 页面加载完成后，设置导航栏的点击事件监听器
document.addEventListener("DOMContentLoaded", () => {
  const navStories = document.getElementById("nav-stories");
  const navGenerate = document.getElementById("nav-generate");
  const content = document.getElementById("content");
  const storyGenerator = document.getElementById("story-generator");

  function loadStoryData() {
    // 这里应该是加载故事数据的函数，例如：
    // content.innerHTML = ...;
    // 由于具体加载逻辑依赖于您的应用，这里只提供一个示例函数。
    console.log("Loading story data...");
  }

  navStories.addEventListener("click", () => {
    if (!navStories.classList.contains("active")) {
      navStories.classList.add("active");
      navGenerate.classList.remove("active");
      content.style.display = "block";
      storyGenerator.style.display = "none";
      loadStoryData(); // 调用加载故事数据的函数
    }
  });

  navGenerate.addEventListener("click", () => {
    if (!navGenerate.classList.contains("active")) {
      navGenerate.classList.add("active");
      navStories.classList.remove("active");
      content.style.display = "none";
      storyGenerator.style.display = "block";
      // 这里可以添加切换到故事生成器时需要执行的代码
    }
  });
});

async function generateStory() {
  const apiKey = "sk-K231s4pXBHfHz76KNxzBfJxCAWV0V6oAm1L6z8QC8LmkYyLk"; // 替换为你的 OpenAI API 密钥
  const model = "moonshot-v1-8k"; // 替换为你使用的模型
  const apiUrl = "https://api.moonshot.cn/v1/chat/completions";
  const themeInput = document.getElementById("story-theme");
  const storyOutput = document.getElementById("story-output");

  const theme = themeInput.value; // 获取用户输入的主题

  // 按钮变为不可点击，并更改文案
  var btn = document.getElementById("generate-story-btn");
  btn.disabled = true;
  btn.innerHTML = "写故事ing...";

  storyOutput.textContent = "正在写故事...";

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
              "你是一个优秀的作家，擅长根据各类主题，撰写出色的故事。故事要求1000字以上。请用以下格式返回结果：<b> 故事题目（不要出现“故事题目”这4个字）</b>  <br>  故事正文（不要出现“故事正文”这4个字） ",
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
    // 将文本换行符替换为 HTML 换行标签
    const formattedContent = data.choices[0].message.content.replace(
      /\n/g,
      "<br>"
    );
    storyOutput.innerHTML = formattedContent;
    // 按钮变为可点击，并恢复文案
    btn.disabled = false;
    btn.innerHTML = "写故事";
  } catch (error) {
    console.error("There has been a problem with your fetch operation:", error);
    storyOutput.textContent = `无法加载故事：${error.message}`; // 将错误信息显示在页面上
  }
}

// 页面加载完成后，为按钮添加点击事件监听器
document.addEventListener("DOMContentLoaded", () => {
  const generateStoryButton = document.getElementById("generate-story-btn");
  if (generateStoryButton) {
    generateStoryButton.addEventListener("click", generateStory);
  }
});
