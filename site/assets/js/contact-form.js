(function () {
  "use strict";

  var form = document.getElementById("enquiry-form");
  if (!form) return;

  var success = document.getElementById("form-success");

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    var name = form.elements["name"].value.trim();
    var email = form.elements["email"].value.trim();
    var phone = form.elements["phone"].value.trim();
    var business = form.elements["business"].value.trim();
    var service = form.elements["service"].value;
    var message = form.elements["message"].value.trim();

    var bodyLines = [
      "Name: " + name,
      "Email: " + email,
      "Phone: " + (phone || "Not provided"),
      "Business: " + (business || "Not provided"),
      "Service of interest: " + (service || "Not specified"),
      "",
      "Message:",
      message
    ];

    var subject = "Enquiry from Digital Growth Solutions website" + (name ? " — " + name : "");
    var mailto =
      "mailto:rohitramesh988@gmail.com" +
      "?subject=" + encodeURIComponent(subject) +
      "&body=" + encodeURIComponent(bodyLines.join("\n"));

    window.location.href = mailto;

    if (success) {
      success.classList.add("is-visible");
      success.setAttribute("tabindex", "-1");
      success.focus();
    }
  });
})();
