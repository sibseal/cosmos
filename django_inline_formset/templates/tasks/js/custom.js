$(document).ready(function () {
    $('.add-conditions').click(function (ev) {
        ev.preventDefault();
        var count = $('#item-conditions').children().length;
        var tmplMarkup = $('#conditions-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('#item-conditions').append(compiledTmpl);
        $('#id_conditions-TOTAL_FORMS').attr('value', count + 1);
    });
});
$(document).ready(function () {
    $('.add-items').click(function (ev) {
        ev.preventDefault();
        var count = $('#item-items').children().length;
        var tmplMarkup = $('#items-template').html();
        var compiledTmpl = tmplMarkup.replace(/__prefix__/g, count);
        $('#item-items').append(compiledTmpl);
        $('#id_items-TOTAL_FORMS').attr('value', count + 1);
    });
});
