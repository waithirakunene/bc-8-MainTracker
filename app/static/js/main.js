$(document).ready(function() {
    $('#myModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget);
      var url = '/repair/' + button.context.dataset.repairid + '/assign-to'
      $('#assign-to').attr('href', url);
    })
})