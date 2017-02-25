/**
 * JS for mdl-textfield icons
 * Andrew Welleck
 */
$(document).ready(function(){
  $("#username").focus(function(){
    $("#mood").css("color", "#2196F3"); //vivid blue
  });
  $("#username").blur(function(){
    $("#mood").css("color", "#E0E0E0"); //light grey
  });
  $("#password").focus(function(){
    $("#lock").css("color", "#2196F3");
  });
  $("#password").blur(function(){
    $("#lock").css("color", "#E0E0E0");
  });
  $("#email").focus(function(){
    $("#mail").css("color", "#2196F3");
  });
  $("#email").blur(function(){
    $("#mail").css("color", "#E0E0E0");
  });
  $("#first_name").focus(function(){
    $("#account_circle").css("color", "#2196F3");
  });
  $("#first_name").blur(function(){
    $("#account_circle").css("color", "#E0E0E0");
  });
  $("#last_name").focus(function(){
    $("#account_box").css("color", "#2196F3");
  });
  $("#last_name").blur(function(){
    $("#account_box").css("color", "#E0E0E0");
  });
});
