const form = document.getElementById("lead-form");
const status = document.getElementById("form-status");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  status.textContent = "";
  status.className = "";

  const data = Object.fromEntries(new FormData(form));
  if (!data.name || data.name.trim().length < 2) {
    return showError("Введите имя (от 2 символов)");
  }
  if (!data.contact || data.contact.trim().length < 5) {
    return showError("Укажите телефон или @username в Telegram");
  }

  const button = form.querySelector("button");
  button.disabled = true;
  button.textContent = "Отправляю…";

  try {
    const resp = await fetch("/api/lead", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const result = await resp.json();
    if (resp.ok && result.ok) {
      form.reset();
      status.textContent = "Заявка отправлена! Свяжемся с вами в течение рабочего дня. ✅";
      status.className = "ok";
    } else {
      showError(result.error || "Не получилось отправить. Попробуйте ещё раз.");
    }
  } catch {
    showError("Нет связи с сервером. Проверьте интернет и попробуйте ещё раз.");
  } finally {
    button.disabled = false;
    button.textContent = "Отправить заявку";
  }
});

function showError(text) {
  status.textContent = text;
  status.className = "err";
}
