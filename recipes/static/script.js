$(document).ready(function() {

    $('input.search').keyup(function() {
        var query = $(this).val();
        $('div.row.recipe').each(function(index) {
            console.log($(this).find('a').text());
            if ($(this).find('a').text().toLowerCase().includes(query.toLowerCase())) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('button.add').click(function() {
        if ($(this).hasClass('ingredient')) {
            var li = $('ul li').last().clone();
            li.children('input').val('');
            li.appendTo('ul');
        } else {
            var li = $('ol li').last().clone();
            li.children('input').val('');
            li.appendTo('ol');
        }
    });

    $('ul,ol').on('click', 'button.delete', function() {
        if ($(this).parent().siblings().length == 0) {
            $(this).siblings('input').val('');
        } else {
            $(this).parent().remove();
        }
    });

    $('input[name=RecipeName]').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
        }
    });

    $('ul,ol').on('keypress', 'input', function(e) {
        if (e.which == 13) {
            e.preventDefault();
            var li = $(this).parent().clone();
            li.insertAfter($(this).parent());
            var input = li.children('input');
            input.val('');
            input.focus();
        }
    });

    $('ul,ol').on('keydown', 'input', function(e) {
        if (e.keyCode == 8) {
            if ($(this).val() == '' && $(this).parent().siblings().length != 0) {
                e.preventDefault();
                $(this).parent().prev().children('input').focus();
                $(this).parent().remove();
            }
        }
    });

});
