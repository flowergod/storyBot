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
    document.getElementById("latest-story-text").innerHTML =
      stories[0].story;
    // 设置最新故事的日期
    document.getElementById('date').textContent = stories[0].date;
				
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
        if (currentOpenStory && currentOpenStory !== dateEl.nextElementSibling) {
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
