$(document).ready(function() {
    $('#formset-wrapper').formset({
        addText: 'add family member',
        deleteText: 'remove',
        prefix: 'familymember_set'
    });

    // click to add a label...
    $('#add-item').click(function(e) {
      // get the highest number in the set so far.
      var max_n = 0;
      $('#label_table').find('input').each(function() {
        if ($(this)[0].hasAttribute('id')) {
          var n = $(this).attr('id').match(/-[0-9]-/g);
          n = parseInt(id[0].substring(1, id[0].length - 1));
          if (n > max_n) {
            max_n = n;
          }
        }
      });
    
      // make a copy of a new row from the template.
      var new_row = $('#item-tpl').find('tr').clone();
      new_row.find('input').each(function() {
        // update id.
        if ($(this)[0].hasAttribute('id')) {
          var id = $(this).attr('id').replace('nnnn', String(n));
          $(this).attr('id', id);
        }
        // update name.
        if ($(this)[0].hasAttribute('name')) {
          var name = $(this).attr('name').replace('nnnn', String(n));
          $(this).attr('name', name);
        }
      });
      new_row.appendTo('#label_table');
  });
});
