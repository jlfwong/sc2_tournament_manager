window.data = {};
window.anim_over = false;
window.edit_mode = false;

var Workspace = Backbone.Controller.extend({
  routes: {
    "edit": "edit"
  },
  edit: function() {
    function editMode() {
      $('#grid .cell input').show();
      window.edit_mode = true;
    }

    function auth() {
      var pass = window.prompt("Enter password:");
      if (pass == null) return;
      $.post('auth',{password:pass},function(data) {
        if (data == 'ok') {
          editMode();
        } else {
          auth();
        }
      });
    };

    (function waitForIt() {
      if (window.anim_over) {
        auth();
      } else {
        window.setTimeout(waitForIt,250);
      }
    })();
  }
});
new Workspace();
Backbone.history.start();
window.setTimeout(function() {
  window.anim_over = true;
},5500);

function updateTheGrid() {
  var nteams = window.data['teams'].length;
  for (var row = 0; row < nteams; row++) {
    for (var col = 0; col < nteams; col++) {
      $('#grid .cell[data-row=' + row + '][data-col=' + col + ']')
        .trigger('change_winner',[data['results'][row][col]]);
    }
  }
}

(function updateTheData() {
  if (window.edit_mode) return;
  if (window.anim_over) {
    data_fetch(function() {
      updateTheGrid();
      window.setTimeout(updateTheData,10000);
    });
  } else {
    window.setTimeout(updateTheData,250);
  }
})();

function data_fetch(callback) {
  $.getJSON('data.json',function(data) {
    window.data = data;  
    callback && callback();
  });
}

function data_put() {
  $.post('data.json',{
    data: JSON.stringify(window.data)
  },function(data) {
    console.log('put!',data);
    window.data = data;
    updateTheGrid();
  });
}

$('#grid .cell').live('change_winner',function(ev,state) {
  var $cell = $(this);
  var row = $cell.data('row');
  var col = $cell.data('col')
  $cell.
    removeClass('green_win').
    removeClass('red_win').
    find('input').attr('checked',false);

  window.data['results'][row][col] = state;

  switch (state) {
    case 'r':
      $cell.addClass('red_win');
      $cell.find('input').attr('checked',false);
      break;
    case 'g':
      $cell.addClass('green_win');
      $cell.find('input').attr('checked',true);
      break;
  }
});


$('#grid .cell input').live('click',function() {
  var $checkbox = $(this);
  var $cell = $checkbox.parent('.cell');
  var checked = $cell.find('input').attr('checked');
  var row = $cell.data('row');
  var col = $cell.data('col');

  var $compCell = $('#grid .cell[data-row=' + col + '][data-col=' + row + ']');

  data_fetch(function() {
    updateTheGrid();
    if (checked) {
      $cell.trigger('change_winner',['g']);
      $compCell.trigger('change_winner',['r']);
    } else {
      $cell.trigger('change_winner',[' ']);
      $compCell.trigger('change_winner',[' ']);
    }
    window.setTimeout(data_put,200); // Just to be safe
  });
});

data_fetch(function () {
  $(document).ready(function() {
    var grid_left = Math.max(
      160,
      $(window).width()  / 2 - 440 / 2
    );

    var grid_top = Math.max(
      160,
      $(window).height() / 2 - 240 / 2
    );

    function center_setup(template_selector) {
      var $ret = $($(template_selector).html());
      $ret.
        appendTo($('body')).
        css({
          position : 'absolute',
          left     : grid_left + 'px',
          top      : grid_top + 'px'
        }).
        hide();
      return $ret;
    }

    // Grid Setup
    var $grid = center_setup('#grid_template');
    $grid.find('.cell').each(function() {
      var row = $(this).data('row');
      var col = $(this).data('col');
      var result = data['results'][row][col];
      switch(result) {
        case 'x':
          $(this).addClass('grey_out');
          $(this).find('input').remove();
          break;
        case 'r':
          $(this).addClass('red_win');
          break;
        case 'g':
          $(this).addClass('green_win');
          $(this).find('input').attr('checked','checked');
          break;
      }
    });

    // Top Bar Setup
    var $top_bar = center_setup('#top_bar_template');
    $top_bar.find('.rot').each(function(i) {
      $(this).text(data['teams'][i]['name']);
    });

    // Left Bar Setup
    var $left_bar = center_setup('#left_bar_template');
    $left_bar.find('.cell').each(function(i) {
      $(this).text(data['teams'][i]['name']);
    });

    // Team List Setup
    var $team_list = $($('#team_list_template').html());
    $team_list.children('.team_entry').hide().each(function(i) {
      $(this).find('.team_name').text(data['teams'][i]['name']);

      $(this).find('.player').each(function(j) {
        $(this).text(data['teams'][i]['players'][j]);
      });
    });

    $team_list.
      css('position','absolute').
      offset({
          left: grid_left + 295,
          top:  grid_top
      }).
      appendTo($('body'));

    // Logo Setup
    var $logo = $('img#logo_bg');
    $logo.
      offset({
        left: grid_left + 250,
        top:  grid_top  - 150
      });

    var logo_src = $logo.attr('src');
    $logo.attr('src','');
    $logo.attr('src',logo_src);
    $logo.load(function() {
      // Have the image flicker in
      $logo.unbind('load');
      $logo.
        css('opacity',0).
        show().
        animate({opacity:0.3},50).
        animate({opacity:0.0},50).
        animate({opacity:0.3},50).
        animate({opacity:0.0},50).
        animate({opacity:0.3},50).
        animate({opacity:0.0},50).
        delay(500).
        animate({
          opacity: 1,
        },{
          duration: 200
        });

      // Make the logo pulsate
      (function logo_pulse() {
        var cycle_length = 3000;
        $logo
          .animate({opacity:0.6},cycle_length/2)
          .animate({opacity:0.9},cycle_length/2);
        window.setTimeout(logo_pulse,cycle_length);
      })();

      $grid.delay(1000).fadeIn(1500);

      window.setTimeout(function() {
        $top_bar.
          show().
          animate({
            top : '-=150'
          },{
            duration: 500,
            queue: true
          }).
          animate({
            top : '+=10'
          },{
            duration: 500,
            queue: true
          });

        $left_bar.
          show().
          animate({
            left : '-=150'
          },{
            duration: 500,
            queue: true
          }).
          animate({
            left : '+=10'
          },{
            duration: 500,
            queue: true
          });
      },2500);

      $team_list.children('.team_entry').each(function(i) {
        $(this).delay(3500 + i*190).slideDown(150);
      });
    });

    $('#grid .cell').bind('mouseover',function() {
      var row = $(this).data('row');
      var col = $(this).data('col');

      $(this).addClass('hover');

      $('#top_bar .cell').eq(col).addClass('hover');
      $('#left_bar .cell').eq(row).addClass('hover');

      $('#team_list .team_entry').eq(col).addClass('hover');
      $('#team_list .team_entry').eq(row).addClass('hover');
    });

    $('#top_bar .rot, #left_bar .cell').bind('mouseover',function() {
      $('#top_bar .cell, #left_bar .cell, #team_list .team_entry').
        filter(':contains(' + $(this).text() + ')').
        addClass('hover');
    });

    $('#team_list .team_entry').bind('mouseover',function() {
      $('#top_bar .cell, #left_bar .cell, #team_list .team_entry').
        filter(':contains(' + $(this).find('.team_name').text() + ')').
        addClass('hover');
    });

    $('#top_bar .cell, #left_bar .cell, #team_list .team_entry, #grid .cell').bind('mouseout',function() {
      $('#top_bar .cell, #left_bar .cell, #team_list .team_entry, #grid .cell').
        removeClass('hover');
    });
  });
});
