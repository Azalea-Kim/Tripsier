document.querySelector('.previous-button').addEventListener('click', function() {
  const currentDate = new Date(document.querySelector('.date-input').value);
  currentDate.setDate(currentDate.getDate() - 1);
  document.querySelector('.date-input').value = currentDate.toISOString().slice(0, 10);
});

document.querySelector('.next-button').addEventListener('click', function() {
  const currentDate = new Date(document.querySelector('.date-input').value);
  currentDate.setDate(currentDate.getDate() + 1);
  document.querySelector('.date-input').value = currentDate.toISOString().slice(0, 10);
});

// when hovering the .door_open class, a bounce effect will be added
$(".door_open").hover(function(){
    $(this).addClass("fa-bounce");
  }, function(){
    $(this).removeClass("fa-bounce");
  });

// when hovering the .door_close class, a red shaking effect will be added
$(".door_close").hover(function(){
    $(this).addClass("shake");
    $(this).css("color", "red");
    setTimeout(() => {
      $(this).css("color", "");
    }, 300);
  }, function(){
    $(this).removeClass("shake");
  });