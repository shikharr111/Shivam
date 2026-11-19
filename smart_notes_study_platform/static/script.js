// Small client-side enhancements for the StudySpace dashboard.
document.querySelectorAll(".nav-link").forEach(link => {
  link.addEventListener("click", () => {
    document.querySelectorAll(".nav-link").forEach(item => item.classList.remove("active"));
    link.classList.add("active");
  });
});

// Set a helpful minimum date for new task deadlines (today).
const dueDate = document.querySelector('input[name="due_date"]');
if (dueDate) dueDate.min = new Date().toISOString().slice(0, 10);

// Automatically hide success/error messages after a few seconds.
document.querySelectorAll(".flash").forEach(message => {
  setTimeout(() => {
    message.style.transition = "opacity .4s";
    message.style.opacity = "0";
    setTimeout(() => message.remove(), 450);
  }, 3500);
});
