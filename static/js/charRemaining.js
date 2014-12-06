$(function()
{
    var maxLength = $('#textarea').attr('maxlength');        //(1)
    $('#textarea').keyup(function()
    {
        var curLength = $('#textarea').val().length;         //(2)
        $(this).val($(this).val().substr(0, maxLength));     //(3)
        var remaning = maxLength - curLength;
        if (remaning < 0) remaning = 0;
        $('#textareaFeedback').html(remaning + ' осталось символов'); //(4)
        if (remaning < 10)                                           //(5)
        {
            $('#textareaFeedback').addClass('warning')
        }
        else
        {
            $('#textareaFeedback').removeClass('warning')
        }
    })
})