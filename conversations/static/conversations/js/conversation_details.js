// scroll chat to the bottom on page load
function scrollToBottom() {
  const messages = document.querySelector(".messages");
  messages.scrollTop = messages.scrollHeight;
}

scrollToBottom();
