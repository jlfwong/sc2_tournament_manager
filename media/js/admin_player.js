$("[data-sc2ranks-button]").live('click',function() {
    $("form#player_form input").attr({disabled:'disabled'});
    $.ajax({
        url: '/admin/players/player/sc2ranks',
        data: { 
            name:       $('#id_name').val(),
            charcode:   $('#id_charcode').val()
        },
        dataType: 'json',
        success: function(data) {
            if (!data.error) {
                $('#id_league').val({
                    diamond:    'd',
                    platinum:   'p',
                    gold:       'g',
                    silver:     's',
                    bronze:     'b'
                }[data.league]);

                $('#id_race').val({
                    protoss:    'p',
                    terran:     't',
                    zerg:       'z',
                    random:     'r'
                }[data.race]);

                $('#id_charcode').val(data.charcode);
                $('#id_bnet_id').val(data.bnet_id);

                $('#id_portrait_id').val(data.portrait.id);
                $('#id_portrait_row').val(data.portrait.row);
                $('#id_portrait_col').val(data.portrait.col);

                if (data.warning) {
                    alert(data.warning);
                }
            } else {
                alert(data.error);
            }
            $("form#player_form input").attr({disabled:''});
        },
        error: function() {
            $("form#player_form input").attr({disabled:''});
            console.log('shit broke');
        }
    });
});
