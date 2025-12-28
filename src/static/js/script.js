function confirmAction(formElement) {
  // Find the button inside the form that was clicked
  const btn = formElement.querySelector("button[type='submit']");

  // Read data attributes
  const PatientName = btn.getAttribute("data-patient_name");

  // Build a contextual message
  const message = `Are you sure you want to change file status of "${PatientName}"?`;

  // Show confirm dialog
  return confirm(message);
}