$(document).ready(function() {
  var constant = false;
  var isSelected;
  $(".repeat").change(function() {
    if ($(".repeat").val() == 2) {
      $(".day_form").css("display", "initial");
      $(".date_form").css("display", "none");
    } else if ($(".repeat").val() == 1) {
      $(".date_form").css("display", "none");
      $(".day_form").css("display", "none");
    } else {
      $(".day_form").css("display", "none");
      $(".date_form").css("display", "initial");
    }
  });

  Date.prototype.toDateInputValue = function() {
    var local = new Date(this);
    local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
    return local.toJSON().slice(0, 10);
  };

  $("#date").val(new Date().toDateInputValue());

  $(".submition").click(function() {
    document.getElementById("schedule_form").submit();
  });

  $(".coffee").click(function() {
    if (constant != true) {
      this.innerHTML = "Confirm selection";
      $(this).addClass("pending");
      $(".schedule_form").css("display", "none");
      $(".coffee_back").css("display", "initial");
      $(".coffeeOptions").css("display", "flex");
      constant = true;
    } else {
      $(".coffee").html("Choose coffee type");
      $(".schedule_form").css("display", "initial");
      $(".coffee_back").css("display", "none");
      $(".coffeeOptions").css("display", "none");
      $(".extra").val();

      constant = false;
    }
  });

  $(".coffee_back, #program").click(function() {
    if (constant == false) {
    } else {
      $(".coffee").html("Choose beverage type");
      $(".schedule_form").css("display", "initial");
      $(".coffee_back").css("display", "none");
      $(".coffeeOptions").css("display", "none");
      $(".coffee").removeClass("pending");
      $(".coffeeOptions div").removeClass("selected");
      $(".coffeeOptions div p").css("color", "rgb(33, 37, 41)");
      $(".extra").val("");
      constant = false;
    }
  });

  $("#now").click(function() {
    $(".coffeeOptions2 div").removeClass("selected");
    $(".coffeeOptions2 div p").css("color", "rgb(33, 37, 41)");
  });

  $(".coffeeOptions div").click(function() {
    $(".coffeeOptions div").removeClass("selected");
    $(".coffeeOptions div p").css("color", "rgb(33, 37, 41)");
    $(this).addClass("selected");
    $(this)
      .children("p")
      .css("color", "blue");
    $(".extra").val(
      $(this)
        .children("p")
        .html()
    );
  });

  $(".coffeeOptions2 div").click(function() {
    $(".coffeeOptions2 div").removeClass("selected");
    $(".coffeeOptions2 div p").css("color", "rgb(33, 37, 41)");
    $(this).addClass("selected");
    $(this)
      .children("p")
      .css("color", "blue");
    $(".extra2").val(
      $(this)
        .children("p")
        .html()
    );
  });

  $(".schedule_form2 input.coffee2").click(function() {
    if ($(".extra2").val() == "Espresso") {
      $(".schedule_form2").attr("action", `/makeE/${$(".cups2").val()}`);
    } else if ($(".extra2").val() == "Americano") {
      $(".schedule_form2").attr("action", `/makeA/${$(".cups2").val()}`);
    } else if ($(".extra2").val() == "Double Espresso") {
      $(".schedule_form2").attr("action", `/makeDE/${$(".cups2").val()}`);
    } else {
      $(".schedule_form2").attr("action", `/makeHW/${$(".cups2").val()}`);
    }
    document.getElementById("schedule_form2").submit();
  });

  $(".isActive").click(function() {
    if ($(this)[0].innerText == "OFF") {
      $(location).attr("href", "/on");
    } else {
      $(location).attr("href", "/off");
    }
  });

  if ($(".isActive")[0].innerText == "OFF") {
    $(".isActive").css("border-color", "red");
    $(".isActive").css("background-color", "red");
    $(".something").css(
      "box-shadow",
      "0 4px 8px 0 #ffcccb, 0 6px 20px 0 #ffcccb"
    );
  } else {
    $(".isActive").css("border-color", "green");
    $(".isActive").css("background-color", "green");
    $(".something").css(
      "box-shadow",
      "0 4px 8px 0 #66ff99, 0 6px 20px 0 #66ff99"
    );
  }

  $("#viewSchedule").click(function() {
    $(location).attr("href", "/get_schedules");
  });

  // if()

  $(".notification span").click(function() {
    $(this)
      .parent()
      .fadeToggle();
    // console.log($(this).parent());
  });

  if($(".notif p").html() == "0"){
    $(".isbeingmade").fadeToggle();
  } else if($(".notif p").html() == "1"){
    $(".ismissing").fadeToggle();
  } else if($(".notif p").html() == "2"){
    $(".isnoton").fadeToggle();
  } else if($(".notif p").html() == "3"){
    $(".isbusy").fadeToggle();
  }

});

AOS.init();
