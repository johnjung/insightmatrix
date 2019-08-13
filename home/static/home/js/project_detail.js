function get_comparison(comparisons, label_one, label_two) {
  for (var c=0; c < comparisons.length; c++) {
    if ((comparisons[c][0] == label_one && comparisons[c][1] == label_two) ||
        (comparisons[c][0] == label_two && comparisons[c][1] == label_one)) {
      return parseFloat(comparisons[c][2]) / 4.0;
    }
  }
  return 0;
}

$.getJSON('/json', function(data) {
  // grid size.
  var grid = 20;
  
  // number of cells. 
  var cells = data.labels.length;
  
  // label width, in pixels.
  var label_width = 100;
  
  // pixel offset for labels.
  var y_label_offset = 14;
  var x_label_offset = 8;
  
  // class names for gray boxes here.
  var grays = ['rect_gray_0', 'rect_gray_1', 'rect_gray_2', 'rect_gray_3'];
  
  // item labels, in order.
  var labels = data.labels;
  
  // similarity scores for each item.
  var similarity = [];
  for (var y = 0; y < labels.length; y++) {
      for (var x = 0; x < labels.length; x++) {
          if (x == 0) {
              similarity.push([]);
          }
          similarity[y].push(get_comparison(data.comparisons, labels[y], labels[x]));
      }
  }
  
  // save the x/y grid position of mousedown events. 
  var mousedown_x = null;
  var mousedown_y = null;
  
  // save the label index for dragging. 
  var label_index = null;
  
  var drag_active = false;
  var drag_element = null;
  var drag_element_index = null;
  var drag_element_initial_x = null;
  var drag_element_initial_y = null;
  var drag_initial_x = null;
  var drag_initial_y = null;
  var drag_current_x = null;
  var drag_current_y = null;
  var drag_offset_x = null;
  var drag_offset_y = null;
  
  // a generic function to make SVG elements.
  function make_element(name, attribs) {
    var e = document.createElementNS('http://www.w3.org/2000/svg', name);
    for (var k in attribs) {
       if (attribs.hasOwnProperty(k)) {
         e.setAttribute(k, attribs[k]);
       }
    }
    return e;
  }
  
  function get_mouse_event_grid_coordinates(e) {
    var r = e.currentTarget.getBoundingClientRect();
    var x = Math.floor((e.clientX - r.x - label_width) / grid);
    var y = Math.floor((e.clientY - r.y - label_width) / grid);
    if (x >= 0 && y >= 0) {
      return {
        'x': x,
        'y': y
      };
    } else {
      return {
        'x': undefined,
        'y': undefined
      };
    }
  }

  function get_mouse_event_label_index(e) {
    var r = e.currentTarget.getBoundingClientRect();
    var x = e.clientX - r.x;
    var y = e.clientY - r.y;
    if (x < 100) {
      return Math.floor((y - 100) / grid);
    } else if (y < 100) {
      return Math.floor((x - 100) / grid);
    } else {
      return undefined;
    }
  }
  
  function reorder_similarity(from, to) {
    similarity.splice(to, 0, similarity.splice(from, 1)[0]);
    for (var y = 0; y < labels.length; y++) {
      similarity[y].splice(to, 0, similarity[y].splice(from, 1)[0]);
    }
  }
  
  function recolor_grid() {
      for (var y = 0; y < labels.length; y++) {
          for (var x = 0; x < labels.length; x++) {
              var id = 'rect_' + y + '_' + x;
              var g = Math.round(similarity[y][x] * grays.length);
              for (var i = 0; i < grays.length; i++) {
                  if (i == g) {
                      document.getElementById(id).classList.add(grays[i]);
                  } else {
                      document.getElementById(id).classList.remove(grays[i]);
                  }
              }
          }
      }
  }
  
  function reorder_labels(a, b) {
    // move element at position a to position b
    if (a >= labels.length) {
      var k = b - labels.length + 1;
      while (k--) {
        labels.push(undefined);
      }
    }
    labels.splice(b, 0, labels.splice(a, 1)[0]);
  }
  
  function reposition_labels(skip_index) {
    for (var i = 0; i < labels.length; i++) {
      if (i != skip_index) {
        document.getElementById('y_' + labels[i]).setAttribute('y', i * grid + y_label_offset);
        document.getElementById('x_' + labels[i]).setAttribute('x', i * grid);
        document.getElementById('x_' + labels[i]).setAttribute('transform', 'rotate(270, ' + i * grid + ', -5)');
      }
    }
  }
  
  function dragstart(e) {
    if (e.target.getAttribute('draggable') == 'true') {
      drag_active = true;
      drag_element = e.target;
      drag_element_index = labels.indexOf(drag_element.id.substring(2));
      drag_element_initial_x = parseInt(drag_element.getAttribute('x'));
      drag_element_initial_y = parseInt(drag_element.getAttribute('y'));
      if (e.type === "touchstart") {
        drag_initial_x = e.touches[0].clientX;
        drag_initial_y = e.touches[0].clientY;
      } else {
        drag_initial_x = e.clientX;
        drag_initial_y = e.clientY;
      }
    }
  }
  
  function dragend(e) {
    drag_active = false;
    if (drag_element == null) {
      return;
    }
    if (drag_element.id.startsWith('y_')) {
      var index_offset = Math.round(drag_offset_y / grid);
      if (index_offset != 0) {
        reorder_labels(drag_element_index, drag_element_index + index_offset);
      }
    } else {
      var index_offset = Math.round(drag_offset_x / grid);
      if (index_offset != 0) {
        reorder_labels(drag_element_index, drag_element_index + index_offset);
      }
    }
    reposition_labels(-1);
    reorder_similarity(drag_element_index, drag_element_index + index_offset);
    recolor_grid();
    drag_element = drag_initial_x = drag_initial_y = drag_element_initial_x = drag_element_initial_y = null;
  }
  
  function drag(e) {
    if (drag_active) {
      e.preventDefault();
      if (e.type === "touchmove") {
        drag_current_x = e.touches[0].clientX;
        drag_current_y = e.touches[0].clientY;
      } else {
        drag_current_x = e.clientX;
        drag_current_y = e.clientY;
      }
  
      if (drag_element.id.startsWith('y_')) {
        drag_offset_y = drag_current_y - drag_initial_y;
        drag_element.setAttribute('y', drag_element_initial_y + drag_offset_y);
      } else {
        drag_offset_x = drag_current_x - drag_initial_x;
        drag_element.setAttribute('x', drag_element_initial_x + drag_offset_x);
        drag_element.setAttribute('transform', 'rotate(270, ' + String(drag_element_initial_x + drag_offset_x) + ', -5)');
      }
    }
  }
  
  function setTranslate(x, y, e) {
    e.style.transform = "translate3d(" + x + "px, " + y + "px, 0)";
  }
  
  // add boxes.
  for (var y = 0; y < 30; y++) {
    for (var x = 0; x < 30; x++) {
      var id = 'rect_' + x + '_' + y;
      var r = make_element('rect', {'id': id, 'x': x * grid, 'y': y * grid, 'width': grid, 'height': grid});
      document.querySelector('svg').append(r);
    }
  }
  // add horizontal grid lines.
  for (var y = 0; y <= grid * cells; y += grid) {
    var l = make_element('line', {
      'x1': 0,
      'y1': y, 
      'x2': grid * cells, 
      'y2': y, 
      'stroke': '#aaa'
    });
    l.setAttribute('stroke-width', y == grid * cells ? 2 : 1);
    document.querySelector('svg').append(l);
  }
  // add vertical grid lines. 
  for (var x = 0; x <= grid * cells; x += grid) {
    var l = make_element('line', {
      'x1': x, 
      'y1': 0, 
      'x2': x, 
      'y2': grid * cells, 
      'stroke': '#aaa'
    });
    l.setAttribute('stroke-width', x == grid * cells ? 2 : 1);
    document.querySelector('svg').append(l);
  }
  // add labels.
  for (var l = 0; l < labels.length; l++) {
    var t = make_element('text', {
      'draggable': true,
      'id': 'y_' + labels[l],
      'x': -5, 
      'y': l * grid + y_label_offset, 
      'fill': 'black', 
      'text-anchor': 'end'
    });
    t.append(document.createTextNode(labels[l]));
    //t.addEventListener('touchstart', dragstart, false);
    //t.addEventListener('touchend', dragend, false);
    //t.addEventListener('touchmove', drag, false);
    //t.addEventListener('mousedown', dragstart, false);
    //t.addEventListener('mouseup', dragend, false);
    //t.addEventListener('mousemove', drag, false);
    document.querySelector('svg').append(t);
  
    var t = make_element('text', {
      'draggable': true,
      'id': 'x_' + labels[l],
      'x': l * grid, 
      'y': x_label_offset, 
      'fill': 'black', 
      'transform': 'rotate(270, ' + l * grid + ', -5)'
    });
    t.append(document.createTextNode(labels[l]));
    //t.addEventListener('touchstart', dragstart, false);
    //t.addEventListener('touchend', dragend, false);
    //t.addEventListener('touchmove', drag, false);
    //t.addEventListener('mousedown', dragstart, false);
    //t.addEventListener('mouseup', dragend, false);
    //t.addEventListener('mousemove', drag, false);
    document.querySelector('svg').append(t);
  }
  
  /*
  document.querySelector('svg').addEventListener('click', function(e) {
    var p = get_mouse_event_grid_coordinates(e);
    if (!isNaN(p.x) && !isNaN(p.y) && p.x != p.y) {
      var s = Math.round(similarity[p.y][p.x] * grays.length) + 1;
      if (s >= grays.length) {
          s = 0;
      }
      s = s / grays.length;
      similarity[p.y][p.x] = s;
      similarity[p.x][p.y] = s;
      recolor_grid();
    } else {
      // var l = get_mouse_event_label_index(e);
      // reorder_labels(l, l < labels.length - 1 ? l + 1 : 0);
      // reposition_labels();
      // reorder_similarity(l, l < labels.length - 1 ? l + 1 : 0);
      // recolor_grid();
    }
  });
  */
  
  // color in the grid.
  recolor_grid();
});
