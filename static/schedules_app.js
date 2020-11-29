$(document).ready(function() {
  if ($(".isActive")[0].innerText == "OFF") {
    $(".isActive").css("border-color", "red");
    $(".isActive").css("background-color", "red");
  } else {
    $(".isActive").css("border-color", "green");
    $(".isActive").css("background-color", "green");
  }

  $(".buttonn button").click(function() {
    $(location).attr("href", "/home");
  });
});
