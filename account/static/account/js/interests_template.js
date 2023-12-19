function toggleCheckbox(label, color) {
  const checkbox = label.querySelector('input[type="checkbox"]');

  checkbox.checked = !checkbox.checked;
  if (checkbox.checked) {
    label.style.backgroundColor = color;
    label.style.color = "white";
  } else {
    label.style.backgroundColor = "white";
    label.style.color = "black";
  }
}
