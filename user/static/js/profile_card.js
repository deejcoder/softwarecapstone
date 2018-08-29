$(document).ready(function () {
    
    // route clicking on the avatar to the file input
    $("img[id='avatar']").click(function () {
        $("input[id='upload_avatar']").click();
    });

    // submit the avatar form once a file has been selected
    $("input[id='upload_avatar']").change(function () {
        $("form[id='avatar_form']").submit()
    })
});