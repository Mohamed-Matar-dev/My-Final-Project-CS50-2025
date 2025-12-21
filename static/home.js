// Ongoin tasks ordered list 
const ongoingContainer = document.querySelector("#ongoing-tasks");
// completed tasks ordered list
const completedContainer = document.querySelector("#completed-tasks");
// check box for all the list items
const checkBox = document.querySelectorAll('input[type="checkbox"]');

// menu to show options on the page 
const taskMenuBtn = document.querySelectorAll(".task-menu-btn");

const editBtn = document.querySelectorAll(".edit-btn");
const deleteBtn = document.querySelectorAll(".delete-btn");

function checkEmptyState() {
  const ongoingTasks = ongoingContainer.querySelectorAll("li");
  const completeTasks = completedContainer.querySelectorAll("li");

  const emptyMessage1 = document.querySelector("#empty-message-ongoing");
  const emptyMessage2 = document.querySelector("#empty-message-complete");

  emptyMessage1.classList.toggle("d-none", ongoingTasks.length > 0);
  emptyMessage2.classList.toggle("d-none", completeTasks.length > 0);
}


// making the check box works as intented
checkBox.forEach(box => {
  box.addEventListener("change", (e) => {
    const li = e.target.closest("li");
    if (!li) return;

    // checking if task completet
    const completed = e.target.checked;

    // Send Update database request to app.py
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

    checkEmptyState(); 
  });
});


// the logic so each menu button work as way to show options
taskMenuBtn.forEach((btn) => {
  btn.addEventListener("click", (event) => {
    event.stopPropagation();
    const li = event.target.closest("li");
    const options = li.querySelector(".task-options");
    options.classList.toggle("d-none");
  });
});




// delete task logic 
deleteBtn.forEach(btn => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const li = e.target.closest("li");
    const taskId = li.id;
    // sent post request to flask
    const confirmed = confirm("Are you sure you want to delete this task?");
    if (!confirmed) return;

    btn.disabled = true;
    fetch("/delete-task", {
      method: "POST",
      headers: {"Content-type": "application/json"},
      body: JSON.stringify({id: taskId})
    }).then(response => {         // after the request sent wait for the return
      if (response.ok){
        li.remove(); // remove from the DOM
        checkEmptyState();
      }else {
        alert("Faild to delete task");
      }
    }).finally(() => btn.disabled = false);

    
  });
});

editBtn.forEach(btn =>{
  btn.addEventListener("click", (e) => {
    e.stopPropagation();
    const li = e.target.closest("li");
    const label = li.querySelector("label");
    const taskId = li.id;

    const currentText = label.textContent;
    const newText = prompt("Edit task title", currentText);
    if (newText && newText !== currentText){
       fetch("/edit-task", {
      method: "POST",
      headers: {"Content-type": "application/json"},
      body: JSON.stringify({id: taskId, title: newText})
    }).then(response => {
      if (response.ok){
        label.textContent = newText; //update on the page
      }else {
        alert("Faild to edit task");
      }
    }).finally(() => btn.disabled = false);

    }

  });
});

document.addEventListener("click", () => {
  document.querySelectorAll(".task-options")
    .forEach(opt => opt.classList.add("d-none"));
});

checkEmptyState();