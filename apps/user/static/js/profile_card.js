$(document).ready(function () {
    
    // route clicking on the avatar to the file input
    $("img[id='avatar']").click(function () {
        $("input[id='upload_avatar']").click();
    });

    $("input[id='upload_avatar']").change(function () {
        var reader = new FileReader();

        reader.onload = function(e) {
            $("img[id='avatar']").attr("src", e.target.result);
        }

        reader.readAsDataURL(this.files[0]);
    });

    // submit the avatar form once a file has been selected
    //$("input[id='upload_avatar']").change(function () {
    //    $("form[id='avatar_form']").submit()
    //})
});