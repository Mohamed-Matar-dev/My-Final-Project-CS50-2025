const ongoingContainer = document.querySelector("#ongoing-tasks");
const completedContainer = document.querySelector("#completed-tasks");

const checkBox = document.querySelectorAll('input[type="checkbox"]');

checkBox.forEach(box => {
  box.addEventListener("change", (e) => {
    const li = e.target.closest("li");
    if (!li) return;

    const completed = e.target.checked;

    // Update database
    fetch("/complete-task", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ id: li.id, completed })
    });

    // Move element to the correct container
    if (completed) {
      completedContainer.appendChild(li);
      li.querySelector("label").classList.add("text-decoration-line-through");
    } else {
      ongoingContainer.appendChild(li);
      li.querySelector("label").classList.remove("text-decoration-line-through");
    }
  });
});
