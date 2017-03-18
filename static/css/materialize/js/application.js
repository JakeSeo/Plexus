Turbolinks.enableProgressBar();

$(document).on('ready page:load', function () {
  Waves.displayEffect();
  Materialize.updateTextFields();
  $('select').material_select();
  $(".button-collapse").sideNav();
  $(".dropdown-button").dropdown();
  $('body').addClass('loaded');
  $('.collapsible').collapsible({
    accordion : false
  });
});

$(document).on('page:load', function () {
  $('input, textarea').characterCounter();
  $('ul.tabs').tabs();
});
$('.timepicker').pickatime({
    twelvehour: true,
    donetext: 'Done',
    beforeShow: function() {
      activeElement = $(document.activeElement)
      activeForm = activeElement.closest('form')[0]

      // Remove existing validation errors
      activeForm.ClientSideValidations.removeError(activeElement)

      // Prevent a validation error occurring when element un-focusses
      activeElement.disableClientSideValidations();
    },
    afterDone: function() {
      activeElement = $(document.activeElement)
      $(activeElement).enableClientSideValidations();
    }
  });