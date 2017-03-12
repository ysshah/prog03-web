$(document).ready(function() {

    $('input.search').keyup(function() {
        var query = $(this).val();
        $('a.recipe').each(function(index) {
            if ($(this).find('span.name div').text().toLowerCase().includes(query.toLowerCase())) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('div.add-button').click(function() {
        if ($(this).hasClass('ingredient')) {
            var li = $('ul li').last().clone();
            li.children('input').val('');
            li.appendTo('ul');
        } else {
            var li = $('ol li').last().clone();
            li.children('textarea').val('');
            li.children('textarea').removeAttr('style');
            li.appendTo('ol');
        }
    });

    $('ul,ol').on('click', 'div.delete', function() {
        if ($(this).parent().siblings().length == 0) {
            $(this).siblings('input, textarea').val('');
        } else {
            $(this).parent().remove();
        }
    });

    $('input[name=RecipeName]').keypress(function(e) {
        if (e.which == 13) {
            e.preventDefault();
        }
    });

    $('ul').on('keypress', 'input', function(e) {
        if (e.which == 13) {
            e.preventDefault();
            var li = $(this).parent().clone();
            li.insertAfter($(this).parent());
            var input = li.children('input');
            input.val('');
            input.focus();
        }
    });

    $('ol').on('keypress', 'textarea', function(e) {
        if (e.which == 13) {
            e.preventDefault();
            var li = $(this).parent().clone();
            li.insertAfter($(this).parent());
            var textarea = li.children('textarea');
            textarea.val('');
            textarea.removeAttr('style');
            textarea.focus();
        }
    });

    $('ul').on('keydown', 'input', function(e) {
        if (e.keyCode == 8) {
            if ($(this).val() == '' && $(this).parent().siblings().length != 0) {
                e.preventDefault();
                $(this).parent().prev().children('input').focus();
                $(this).parent().remove();
            }
        }
    });

    $('ol').on('keydown', 'textarea', function(e) {
        if (e.keyCode == 8) {
            if ($(this).val() == '' && $(this).parent().siblings().length != 0) {
                e.preventDefault();
                $(this).parent().prev().children('textarea').focus();
                $(this).parent().remove();
            }
        }
    });

});
